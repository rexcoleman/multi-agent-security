"""Tests for multi-agent network simulation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import Agent, AgentState, AgentType, Task
from src.network import AgentNetwork
from src.trust import ImplicitTrust, ZeroTrust, CapabilityScopedTrust, create_trust_model
from src.attacker import apply_attack


class TestAgent:
    def test_clean_agent_processes_task(self):
        import numpy as np
        agent = Agent(agent_id=0)
        rng = np.random.default_rng(42)
        task = Task(task_id=0, content="test")
        result = agent.process_task(task, rng)
        assert not result.is_poisoned
        assert agent.total_decisions == 1

    def test_compromised_agent_produces_poison(self):
        import numpy as np
        agent = Agent(agent_id=0, compromise_potency=1.0)
        agent.state = AgentState.COMPROMISED
        rng = np.random.default_rng(42)
        task = Task(task_id=0, content="test")
        result = agent.process_task(task, rng)
        assert result.is_poisoned

    def test_poison_rate_tracking(self):
        import numpy as np
        agent = Agent(agent_id=0, compromise_potency=1.0)
        agent.state = AgentState.COMPROMISED
        rng = np.random.default_rng(42)
        for i in range(10):
            agent.process_task(Task(task_id=i, content="t"), rng)
        assert agent.poison_rate == 1.0


class TestTrustModels:
    def test_implicit_accepts_all(self):
        import numpy as np
        trust = ImplicitTrust()
        a1 = Agent(agent_id=0)
        a2 = Agent(agent_id=1)
        task = Task(task_id=0, content="test", is_poisoned=True)
        rng = np.random.default_rng(42)
        assert trust.should_accept(a1, a2, task, rng)
        result = trust.filter_task(a1, task, rng)
        assert result.is_poisoned  # No filtering

    def test_zero_trust_filters_poison(self):
        import numpy as np
        trust = ZeroTrust(verification_prob=1.0)  # 100% detection
        a1 = Agent(agent_id=0)
        task = Task(task_id=0, content="poisoned_test", is_poisoned=True)
        rng = np.random.default_rng(42)
        result = trust.filter_task(a1, task, rng)
        assert not result.is_poisoned

    def test_create_trust_model(self):
        m = create_trust_model("implicit")
        assert isinstance(m, ImplicitTrust)
        m = create_trust_model("zero_trust")
        assert isinstance(m, ZeroTrust)


class TestNetwork:
    def test_hierarchical_topology(self):
        net = AgentNetwork(n_agents=5, topology="hierarchical")
        assert len(net.agents) == 5
        assert net.graph.number_of_nodes() == 5

    def test_flat_topology(self):
        net = AgentNetwork(n_agents=3, topology="flat")
        # All-to-all: 3 * 2 = 6 edges
        assert net.graph.number_of_edges() == 6

    def test_star_topology(self):
        net = AgentNetwork(n_agents=4, topology="star")
        # Hub to 3 + 3 to hub = 6 edges
        assert net.graph.number_of_edges() == 6

    def test_compromise_increases_cascade(self):
        net = AgentNetwork(n_agents=5, topology="hierarchical",
                          trust_model_name="implicit", seed=42)
        apply_attack(net, "naive", target_id=0)
        metrics = net.run_simulation(time_steps=10)
        assert metrics.cascade_rate > 0  # At least initial agent compromised
        assert metrics.poisoned_decisions > 0

    def test_zero_trust_reduces_cascade(self):
        # Implicit trust
        net1 = AgentNetwork(n_agents=5, trust_model_name="implicit", seed=42)
        apply_attack(net1, "naive", target_id=0)
        m1 = net1.run_simulation(time_steps=10)

        # Zero trust
        net2 = AgentNetwork(n_agents=5, trust_model_name="zero_trust", seed=42)
        apply_attack(net2, "naive", target_id=0)
        m2 = net2.run_simulation(time_steps=10)

        # Zero trust should have lower cascade
        assert m2.cascade_rate <= m1.cascade_rate

    def test_isolated_memory_reduces_cascade(self):
        net1 = AgentNetwork(n_agents=5, memory_mode="shared", seed=42)
        apply_attack(net1, "naive", target_id=0)
        m1 = net1.run_simulation(time_steps=10)

        net2 = AgentNetwork(n_agents=5, memory_mode="isolated", seed=42)
        apply_attack(net2, "naive", target_id=0)
        m2 = net2.run_simulation(time_steps=10)

        assert m2.cascade_rate <= m1.cascade_rate

    def test_reproducibility(self):
        """Same seed produces same results."""
        net1 = AgentNetwork(n_agents=5, seed=42)
        apply_attack(net1, "naive", target_id=0)
        m1 = net1.run_simulation(time_steps=5)

        net2 = AgentNetwork(n_agents=5, seed=42)
        apply_attack(net2, "naive", target_id=0)
        m2 = net2.run_simulation(time_steps=5)

        assert m1.cascade_rate == m2.cascade_rate
        assert m1.poison_rate == m2.poison_rate


class TestAttacker:
    def test_naive_attack(self):
        net = AgentNetwork(n_agents=3, seed=42)
        apply_attack(net, "naive", target_id=0)
        assert net.agents[0].state == AgentState.COMPROMISED

    def test_defense_aware_attack(self):
        net = AgentNetwork(n_agents=3, trust_model_name="zero_trust", seed=42)
        apply_attack(net, "defense_aware", target_id=0)
        assert net.agents[0].state == AgentState.COMPROMISED
        assert net.agents[0].compromise_potency == 0.95

    def test_credential_theft(self):
        net = AgentNetwork(n_agents=3, seed=42)
        original_caps = len(net.agents[0].capabilities)
        apply_attack(net, "credential_theft", target_id=0)
        # Should have stolen capabilities from neighbors
        assert len(net.agents[0].capabilities) >= original_caps
