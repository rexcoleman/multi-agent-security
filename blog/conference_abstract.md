# Conference Abstract — AISec Workshop (ACM CCS 2026)

> **Title:** Zero-Trust Cuts Multi-Agent Cascade Poison Rate by 40% — But Adaptive Adversaries Recover 54%
> **Speaker:** Rex Coleman
> **Track:** AI Security / Multi-Agent Systems
> **Length:** 20-30 minutes

## Abstract

Multi-agent AI systems are becoming the dominant production architecture, yet no open-source framework exists for testing their security under compromise. Under implicit trust — the default in CrewAI, AutoGen, and most frameworks — a single compromised agent cascades to 100% of the system regardless of topology, agent type, or memory configuration.

We present the first systematic evaluation of cascade propagation across 3 trust models, 3 topologies, 3 attacker types, 4 agent compositions, and 3 memory modes (6 experiments, 5-seed validation). Zero-trust architecture reduces poison rate by 40 percentage points — the only effective defense. But adaptive adversaries recover 54% of that advantage, pushing poison from 0.583 back to 0.899. Four of six pre-registered hypotheses were refuted: topology, agent type, and memory are irrelevant to cascade dynamics.

Attendees will leave with a concrete threat model for multi-agent compromise, the empirical evidence that zero-trust is necessary but insufficient, and access to the open-source framework for testing their own deployments. Suitable for intermediate to advanced practitioners.

## Bio (100 words)

Rex Coleman is building at the intersection of AI security and ML systems engineering. He spent over a decade at FireEye and Mandiant in data analytics and enterprise sales, working with security teams across Fortune 500 organizations. He is completing his MS in Computer Science at Georgia Tech (Machine Learning specialization), where he researches AI security — adversarial evaluation of ML systems, agent exploitation, and ML governance tooling. He is the creator of govML, an open-source governance framework for ML research projects. CFA charterholder.

## Outline

1. **The Problem** (3 min): Multi-agent systems are the new default. No security testing framework exists. One compromised agent → what happens?
2. **The Framework** (3 min): Simulation-based testbed. Trust models, topologies, attacker types. Design for 8/10 (Gate 0.5).
3. **The Results** (10 min): E2 (zero-trust = only defense), E4 (adaptive adversary recovers 54%). Figures and confidence intervals.
4. **The Negative Results** (5 min): 4/6 hypotheses refuted. Topology, agent type, memory don't matter. Why this narrows the solution space.
5. **Implications** (3 min): Implement zero-trust now. Defense-in-depth against adaptive adversaries. What the agent economy needs.
6. **Demo / Q&A** (5 min): Framework walkthrough. govML governance. Reproducibility.
