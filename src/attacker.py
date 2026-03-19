"""Attacker models for multi-agent security experiments.

Three attacker types:
  - Naive: compromises one agent, doesn't adapt to defenses
  - Defense-aware: modifies attack to bypass known defense (e.g., mimics delegation)
  - Credential-theft: steals agent identity to bypass authentication
"""
from dataclasses import dataclass
from enum import Enum

import numpy as np

from .agent import Agent, AgentState, AgentType
from .network import AgentNetwork


class AttackerType(Enum):
    NAIVE = "naive"
    DEFENSE_AWARE = "defense_aware"
    CREDENTIAL_THEFT = "credential_theft"


@dataclass
class AttackResult:
    attacker_type: str
    target_agent_id: int
    initial_compromise: bool
    final_cascade_rate: float
    final_poison_rate: float
    agents_compromised: int
    total_agents: int

    def to_dict(self) -> dict:
        return {
            "attacker_type": self.attacker_type,
            "target_agent_id": self.target_agent_id,
            "initial_compromise": self.initial_compromise,
            "final_cascade_rate": self.final_cascade_rate,
            "final_poison_rate": self.final_poison_rate,
            "agents_compromised": self.agents_compromised,
            "total_agents": self.total_agents,
        }


def naive_attack(network: AgentNetwork, target_id: int = 0):
    """Naive attacker: directly compromise one agent."""
    network.compromise_agent(target_id)


def defense_aware_attack(network: AgentNetwork, target_id: int = 0):
    """Defense-aware attacker: compromise agent AND boost its potency.

    Models an attacker who knows the defense architecture and crafts
    outputs that look legitimate (higher potency, lower detection rate).
    """
    agent = network.agents[target_id]
    agent.state = AgentState.COMPROMISED
    agent.compromise_potency = 0.95  # Higher potency (mimics legitimate output)

    # If zero-trust, the attacker also tries to craft outputs that pass verification
    if network.trust_model_name == "zero_trust":
        # Reduce verification effectiveness against this specific attacker
        network.trust_model.verification_prob *= 0.5


def credential_theft_attack(network: AgentNetwork, target_id: int = 0):
    """Credential-theft attacker: steal agent identity to bypass auth.

    Models an attacker who compromises one agent AND gains its credentials,
    allowing impersonation. Other agents treat attacker's messages as coming
    from the legitimate agent.
    """
    agent = network.agents[target_id]
    agent.state = AgentState.COMPROMISED
    agent.compromise_potency = 0.95

    # Steal capabilities from neighboring agents
    neighbors = list(network.graph.successors(target_id))
    for n_id in neighbors:
        neighbor = network.agents[n_id]
        agent.capabilities = agent.capabilities | neighbor.capabilities


def apply_attack(
    network: AgentNetwork,
    attacker_type: str,
    target_id: int = 0,
):
    """Apply an attack to the network."""
    attacks = {
        "naive": naive_attack,
        "defense_aware": defense_aware_attack,
        "credential_theft": credential_theft_attack,
    }
    if attacker_type not in attacks:
        raise ValueError(f"Unknown attacker: {attacker_type}. Choose from {list(attacks)}")
    attacks[attacker_type](network, target_id)
