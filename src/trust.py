"""Trust models for multi-agent communication.

Three trust architectures:
  - Implicit: accept all inputs (default in most frameworks)
  - Capability-scoped: accept inputs from agents with matching capabilities
  - Zero-trust: independently verify every input regardless of source
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from .agent import Agent, Task


class TrustModel(ABC):
    """Base trust model for inter-agent communication."""

    @abstractmethod
    def should_accept(
        self,
        receiver: Agent,
        sender: Agent,
        task: Task,
        rng: np.random.Generator,
    ) -> bool:
        """Decide whether receiver should accept task from sender."""

    @abstractmethod
    def filter_task(
        self,
        receiver: Agent,
        task: Task,
        rng: np.random.Generator,
    ) -> Task:
        """Filter/verify task content. May detect and clean poisoned content."""


@dataclass
class ImplicitTrust(TrustModel):
    """Accept all inputs from any agent without verification.

    This is the default in CrewAI, AutoGen, and most multi-agent frameworks.
    Maximum cascade propagation rate — the control condition.
    """

    def should_accept(self, receiver, sender, task, rng):
        return True  # Accept everything

    def filter_task(self, receiver, task, rng):
        return task  # No filtering


@dataclass
class CapabilityScopedTrust(TrustModel):
    """Accept inputs only from agents with matching capability tags.

    Reduces attack surface by limiting which agents can communicate.
    Partially effective: a compromised agent with matching capabilities
    can still propagate poisoned outputs.
    """
    verification_prob: float = 0.3

    def should_accept(self, receiver, sender, task, rng):
        # Accept if capabilities overlap
        overlap = receiver.capabilities & sender.capabilities
        return len(overlap) > 0

    def filter_task(self, receiver, task, rng):
        # Probabilistic verification: may detect poisoned content
        if task.is_poisoned and rng.random() < self.verification_prob:
            return Task(
                task_id=task.task_id,
                content=task.content.replace("poisoned_", ""),
                source_agent_id=task.source_agent_id,
                is_poisoned=False,  # Cleaned
                hop_count=task.hop_count,
            )
        return task


@dataclass
class ZeroTrust(TrustModel):
    """Independently verify every input regardless of source.

    Each agent validates task content before processing.
    Highest defense but also highest latency cost.
    """
    verification_prob: float = 0.8

    def should_accept(self, receiver, sender, task, rng):
        return True  # Accept from anyone, but verify content

    def filter_task(self, receiver, task, rng):
        # High probability of detecting poisoned content
        if task.is_poisoned and rng.random() < self.verification_prob:
            return Task(
                task_id=task.task_id,
                content=task.content.replace("poisoned_", ""),
                source_agent_id=task.source_agent_id,
                is_poisoned=False,  # Cleaned
                hop_count=task.hop_count,
            )
        return task


@dataclass
class TwoOfThreeConstraint(TrustModel):
    """Capability-bounded trust: each agent may hold at most 2 of 3 capability categories.

    Inspired by NVIDIA's NemoClaw/OpenShell pattern. Generalizes the principle of
    least privilege from OS security and network segmentation to multi-agent systems.

    Three capability categories:
      - data_access: can read/write sensitive data stores
      - code_execution: can run arbitrary code
      - external_communication: can make external API calls or send messages

    An agent with at most 2 of 3 cannot independently exfiltrate data (needs
    data_access + external_communication) AND execute arbitrary code. This bounds
    the blast radius of any single compromised agent.

    Verification probability applies when the trust model detects a task that
    requires a capability the receiving agent doesn't hold — it may still accept
    with reduced probability (modeling imperfect enforcement).
    """
    verification_prob: float = 0.6
    # The 3 capability categories — each agent gets exactly 2
    CAPABILITY_CATEGORIES = frozenset({"data_access", "code_execution", "external_communication"})

    def should_accept(self, receiver, sender, task, rng):
        # Accept if sender has at least one capability in common with receiver
        # (agents can communicate within their capability overlap)
        sender_cats = sender.capabilities & self.CAPABILITY_CATEGORIES
        receiver_cats = receiver.capabilities & self.CAPABILITY_CATEGORIES
        overlap = sender_cats & receiver_cats
        if len(overlap) == 0:
            return False  # No capability overlap — reject
        return True

    def filter_task(self, receiver, task, rng):
        # Moderate verification: better than implicit, less than zero-trust
        # The constraint's value is structural (limits blast radius) not just detection
        if task.is_poisoned and rng.random() < self.verification_prob:
            return Task(
                task_id=task.task_id,
                content=task.content.replace("poisoned_", ""),
                source_agent_id=task.source_agent_id,
                is_poisoned=False,
                hop_count=task.hop_count,
            )
        return task


def create_trust_model(name: str, **kwargs) -> TrustModel:
    models = {
        "implicit": ImplicitTrust,
        "capability_scoped": CapabilityScopedTrust,
        "zero_trust": ZeroTrust,
        "two_of_three": TwoOfThreeConstraint,
    }
    if name not in models:
        raise ValueError(f"Unknown trust model: {name}. Choose from {list(models)}")
    return models[name](**kwargs)
