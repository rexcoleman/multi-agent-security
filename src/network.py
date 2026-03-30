"""Multi-agent network: topology, communication, and cascade simulation.

The core simulation engine. Models agents as nodes in a directed graph,
with trust-weighted edges. Simulates task delegation and measures how
compromise propagates through the network over time steps.
"""
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import networkx as nx
import numpy as np

from .agent import Agent, AgentState, AgentType, Task
from .trust import TrustModel, create_trust_model


@dataclass
class CascadeMetrics:
    """Metrics collected during a cascade simulation."""
    time_step: int = 0
    total_agents: int = 0
    compromised_agents: int = 0
    total_decisions: int = 0
    poisoned_decisions: int = 0
    tasks_delegated: int = 0
    tasks_filtered: int = 0
    # Per-timestep tracking
    cascade_over_time: list = field(default_factory=list)
    poison_rate_over_time: list = field(default_factory=list)

    @property
    def cascade_rate(self) -> float:
        if self.total_agents == 0:
            return 0.0
        return self.compromised_agents / self.total_agents

    @property
    def poison_rate(self) -> float:
        if self.total_decisions == 0:
            return 0.0
        return self.poisoned_decisions / self.total_decisions

    def to_dict(self) -> dict:
        return {
            "total_agents": self.total_agents,
            "compromised_agents": self.compromised_agents,
            "cascade_rate": self.cascade_rate,
            "total_decisions": self.total_decisions,
            "poisoned_decisions": self.poisoned_decisions,
            "poison_rate": self.poison_rate,
            "tasks_delegated": self.tasks_delegated,
            "tasks_filtered": self.tasks_filtered,
            "cascade_over_time": self.cascade_over_time,
            "poison_rate_over_time": self.poison_rate_over_time,
        }


class AgentNetwork:
    """A network of agents with configurable topology and trust model."""

    def __init__(
        self,
        n_agents: int,
        topology: str = "hierarchical",
        trust_model_name: str = "implicit",
        agent_types: Optional[dict] = None,
        memory_mode: str = "shared",
        seed: int = 42,
        base_accuracy: float = 0.95,
        compromise_potency: float = 0.90,
        capability_assignment: str = "round_robin",
    ):
        self.n_agents = n_agents
        self.topology = topology
        self.trust_model_name = trust_model_name
        self.memory_mode = memory_mode
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.trust_model = create_trust_model(trust_model_name)
        self.capability_assignment = capability_assignment

        # Create agents
        self.agents = {}
        type_assignments = self._assign_types(n_agents, agent_types)
        for i in range(n_agents):
            caps = self._assign_capabilities(i, n_agents, trust_model_name)
            self.agents[i] = Agent(
                agent_id=i,
                agent_type=type_assignments[i],
                base_accuracy=base_accuracy,
                compromise_potency=compromise_potency,
                capabilities=caps,
            )

        # Build network graph
        self.graph = self._build_topology(topology, n_agents)

        # Shared memory (for memory ablation experiment)
        self.shared_memory: list[Task] = []

    def _assign_capabilities(self, agent_id: int, n_agents: int, trust_model_name: str) -> set:
        """Assign capabilities based on trust model and assignment strategy.

        For two_of_three: each agent gets exactly 2 of 3 capability categories.
        Assignment strategies:
          - round_robin: Agent i gets combo [i % 3]. Maximally distributed.
          - random: Each agent gets a random combo. Uses self.rng for reproducibility.
          - clustered: First N/3 get combo 0, next N/3 get combo 1, rest get combo 2.
        """
        if trust_model_name == "two_of_three":
            categories = ["data_access", "code_execution", "external_communication"]
            combos = [
                {categories[0], categories[1]},           # data + code
                {categories[0], categories[2]},           # data + comm
                {categories[1], categories[2]},           # code + comm
            ]
            if self.capability_assignment == "random":
                combo = combos[int(self.rng.integers(0, 3))]
            elif self.capability_assignment == "clustered":
                third = max(1, n_agents // 3)
                if agent_id < third:
                    combo = combos[0]
                elif agent_id < 2 * third:
                    combo = combos[1]
                else:
                    combo = combos[2]
            else:  # round_robin (default)
                combo = combos[agent_id % 3]
            return {"general", f"role_{agent_id % 3}"} | combo
        else:
            return {"general", f"role_{agent_id % 3}"}

    def _assign_types(self, n: int, type_config: Optional[dict]) -> dict:
        """Assign agent types based on configuration."""
        if type_config is None:
            return {i: AgentType.LLM for i in range(n)}

        assignments = {}
        idx = 0
        for type_name, count in type_config.items():
            for _ in range(count):
                if idx < n:
                    assignments[idx] = AgentType(type_name)
                    idx += 1
        # Fill remaining with LLM
        while idx < n:
            assignments[idx] = AgentType.LLM
            idx += 1
        return assignments

    def _build_topology(self, topology: str, n: int) -> nx.DiGraph:
        """Build directed graph for agent communication."""
        G = nx.DiGraph()
        G.add_nodes_from(range(n))

        if topology == "hierarchical":
            # Tree: agent 0 is root, each agent delegates to children
            for i in range(n):
                left = 2 * i + 1
                right = 2 * i + 2
                if left < n:
                    G.add_edge(i, left)
                    G.add_edge(left, i)
                if right < n:
                    G.add_edge(i, right)
                    G.add_edge(right, i)

        elif topology == "flat":
            # All-to-all communication
            for i in range(n):
                for j in range(n):
                    if i != j:
                        G.add_edge(i, j)

        elif topology == "star":
            # Hub (agent 0) connects to all; others only through hub
            for i in range(1, n):
                G.add_edge(0, i)
                G.add_edge(i, 0)

        else:
            raise ValueError(f"Unknown topology: {topology}")

        return G

    def compromise_agent(self, agent_id: int):
        """Compromise a specific agent (the initial attack)."""
        self.agents[agent_id].state = AgentState.COMPROMISED

    def run_simulation(self, time_steps: int = 20, tasks_per_step: int = 5) -> CascadeMetrics:
        """Run cascade simulation for N time steps.

        Each time step:
        1. Root agent receives new tasks
        2. Tasks are delegated through the network
        3. Each agent processes or delegates based on topology
        4. Compromised outputs propagate if trust model allows
        5. Agents that receive poisoned tasks may become compromised
        """
        metrics = CascadeMetrics(total_agents=self.n_agents)
        task_counter = 0

        for t in range(time_steps):
            step_decisions = 0
            step_poisoned = 0

            # Generate new tasks at root/entry agents
            entry_agents = self._get_entry_agents()
            tasks = []
            for _ in range(tasks_per_step):
                tasks.append(Task(task_id=task_counter, content=f"task_{task_counter}"))
                task_counter += 1

            # Process tasks through network (BFS from entry agents)
            for task in tasks:
                self._propagate_task(task, entry_agents, metrics)

            # Count cascade state
            for agent in self.agents.values():
                step_decisions += agent.total_decisions
                step_poisoned += agent.poisoned_decisions

            # Track per-timestep metrics
            compromised_count = sum(
                1 for a in self.agents.values() if a.state == AgentState.COMPROMISED
            )
            metrics.cascade_over_time.append(compromised_count / self.n_agents)

            total_d = sum(a.total_decisions for a in self.agents.values())
            poisoned_d = sum(a.poisoned_decisions for a in self.agents.values())
            metrics.poison_rate_over_time.append(
                poisoned_d / total_d if total_d > 0 else 0.0
            )

        # Final metrics
        metrics.compromised_agents = sum(
            1 for a in self.agents.values() if a.state == AgentState.COMPROMISED
        )
        metrics.total_decisions = sum(a.total_decisions for a in self.agents.values())
        metrics.poisoned_decisions = sum(a.poisoned_decisions for a in self.agents.values())
        metrics.time_step = time_steps

        return metrics

    def _get_entry_agents(self) -> list[int]:
        """Get agents that receive external tasks (entry points)."""
        if self.topology == "hierarchical":
            return [0]  # Root
        elif self.topology == "star":
            return [0]  # Hub
        else:  # flat
            return [0]  # Arbitrary entry point

    def _propagate_task(self, task: Task, entry_agents: list[int], metrics: CascadeMetrics):
        """Propagate a task through the network via delegation."""
        queue = [(agent_id, task) for agent_id in entry_agents]
        visited = set()

        while queue:
            agent_id, current_task = queue.pop(0)
            if agent_id in visited:
                continue
            visited.add(agent_id)

            agent = self.agents[agent_id]

            # Agent processes task
            output_task = agent.process_task(current_task, self.rng)

            # Write to shared memory if enabled
            if self.memory_mode == "shared":
                self.shared_memory.append(output_task)

            # Cascade: if agent received poisoned task and isn't already compromised,
            # it may become compromised (modeling gradual trust erosion)
            if current_task.is_poisoned and agent.state == AgentState.CLEAN:
                # Probability of compromise depends on trust model
                compromise_prob = self._cascade_probability(agent, current_task)
                if self.rng.random() < compromise_prob:
                    agent.state = AgentState.COMPROMISED

            # Delegate to neighbors
            neighbors = list(self.graph.successors(agent_id))
            if neighbors:
                # Delegate to a subset of neighbors
                n_delegates = min(len(neighbors), 2)
                delegates = self.rng.choice(
                    neighbors, size=n_delegates, replace=False
                )
                for neighbor_id in delegates:
                    neighbor = self.agents[neighbor_id]

                    # Trust model decides acceptance
                    if self.trust_model.should_accept(neighbor, agent, output_task, self.rng):
                        # Trust model may filter/clean the task
                        filtered_task = self.trust_model.filter_task(
                            neighbor, output_task, self.rng
                        )
                        if filtered_task.is_poisoned != output_task.is_poisoned:
                            metrics.tasks_filtered += 1

                        queue.append((neighbor_id, filtered_task))
                        metrics.tasks_delegated += 1

            # Shared memory read: agents read from shared memory
            if self.memory_mode == "shared" and len(self.shared_memory) > 0:
                # Read most recent entry from shared memory
                mem_task = self.shared_memory[-1]
                if mem_task.is_poisoned and agent.state == AgentState.CLEAN:
                    if self.rng.random() < 0.08:  # Memory-based compromise (tuned)
                        agent.state = AgentState.COMPROMISED

    def _cascade_probability(self, agent: Agent, task: Task) -> float:
        """Probability that a poisoned task compromises a clean agent."""
        base_prob = 0.15  # Base cascade probability (tuned for differentiation)

        # Trust model reduces cascade probability
        if self.trust_model_name == "zero_trust":
            base_prob *= 0.2
        elif self.trust_model_name == "two_of_three":
            base_prob *= 0.35  # Between capability_scoped (0.5) and zero_trust (0.2)
        elif self.trust_model_name == "capability_scoped":
            base_prob *= 0.5

        # Agent type affects susceptibility
        if agent.agent_type == AgentType.RULE_BASED:
            base_prob *= 0.3  # Rule-based agents are more resistant
        elif agent.agent_type == AgentType.RL:
            base_prob *= 1.2  # RL agents slightly more susceptible

        # Memory isolation reduces cascade
        if self.memory_mode == "isolated":
            base_prob *= 0.5
        elif self.memory_mode == "partitioned":
            base_prob *= 0.7

        return min(base_prob, 1.0)

    def reset(self):
        """Reset all agents to clean state."""
        for agent in self.agents.values():
            agent.state = AgentState.CLEAN
            agent.reset_counters()
        self.shared_memory.clear()
