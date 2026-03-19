"""Agent model for multi-agent security simulation.

Each agent processes tasks, may delegate to neighbors, and can be compromised.
Compromise propagates through trust-weighted edges in the agent network.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import numpy as np


class AgentType(Enum):
    LLM = "llm"
    RL = "rl"
    RULE_BASED = "rule_based"


class AgentState(Enum):
    CLEAN = "clean"
    COMPROMISED = "compromised"


@dataclass
class Task:
    """A unit of work passed between agents."""
    task_id: int
    content: str
    source_agent_id: Optional[int] = None
    is_poisoned: bool = False
    hop_count: int = 0


@dataclass
class Agent:
    """An agent in a multi-agent system."""
    agent_id: int
    agent_type: AgentType = AgentType.LLM
    state: AgentState = AgentState.CLEAN
    base_accuracy: float = 0.95
    compromise_potency: float = 0.90
    capabilities: set = field(default_factory=lambda: {"general"})
    # Track decisions for analysis
    total_decisions: int = 0
    poisoned_decisions: int = 0
    tasks_received: int = 0
    tasks_delegated: int = 0

    def process_task(self, task: Task, rng: np.random.Generator) -> Task:
        """Process an incoming task. May produce poisoned output if compromised."""
        self.tasks_received += 1
        self.total_decisions += 1

        if self.state == AgentState.COMPROMISED:
            # Compromised agent produces poisoned output with potency probability
            if rng.random() < self.compromise_potency:
                self.poisoned_decisions += 1
                return Task(
                    task_id=task.task_id,
                    content=f"poisoned_{task.content}",
                    source_agent_id=self.agent_id,
                    is_poisoned=True,
                    hop_count=task.hop_count + 1,
                )

        # Clean agent or compromise didn't trigger
        # But if the input was poisoned, the agent may not detect it
        output_poisoned = task.is_poisoned  # Pass-through by default
        if task.is_poisoned:
            self.poisoned_decisions += 1

        return Task(
            task_id=task.task_id,
            content=task.content,
            source_agent_id=self.agent_id,
            is_poisoned=output_poisoned,
            hop_count=task.hop_count + 1,
        )

    @property
    def poison_rate(self) -> float:
        if self.total_decisions == 0:
            return 0.0
        return self.poisoned_decisions / self.total_decisions

    def reset_counters(self):
        self.total_decisions = 0
        self.poisoned_decisions = 0
        self.tasks_received = 0
        self.tasks_delegated = 0
