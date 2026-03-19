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


def create_trust_model(name: str, **kwargs) -> TrustModel:
    models = {
        "implicit": ImplicitTrust,
        "capability_scoped": CapabilityScopedTrust,
        "zero_trust": ZeroTrust,
    }
    if name not in models:
        raise ValueError(f"Unknown trust model: {name}. Choose from {list(models)}")
    return models[name](**kwargs)
