# Conference Abstract — AISec Workshop (ACM CCS 2026)

> **Title:** Zero-Trust Cuts Multi-Agent Cascade Poison Rate by 40% — But Adaptive Adversaries Recover 54%
> **Speaker:** Rex Coleman
> **Track:** AI Security / Multi-Agent Systems
> **Length:** 20-30 minutes

## Abstract

Multi-agent AI systems are becoming the dominant production architecture, yet no open-source framework exists for testing their security under compromise. We present the first systematic evaluation of cascade propagation in multi-agent systems, measuring how a single compromised agent's poisoned outputs affect downstream decisions across 3 trust models, 3 network topologies, 3 attacker types, 4 agent compositions, and 3 memory modes — totaling 6 experiments with 5-seed validation.

Key findings:
1. **Under implicit trust (the default in CrewAI, AutoGen, and most frameworks), cascade reaches 100% regardless of system size, topology, agent type, or memory configuration.** The default provides zero containment.
2. **Zero-trust architecture reduces poison rate by 40 percentage points** (0.974 → 0.583) — the only effective defense. Capability-scoping achieves only 7pp reduction.
3. **Adaptive adversaries recover 54% of zero-trust's advantage.** A defense-aware attacker pushes poison rate from 0.583 back to 0.899, demonstrating that static verification is insufficient.
4. **4 of 6 pre-registered hypotheses were refuted**, yielding practitioner-relevant negative results: topology, agent type, and memory mode are irrelevant to cascade dynamics. The solution space is narrower than expected.

We release the framework as open source with configurable parameters, 16 tests, and full reproducibility.

## Bio (100 words)

Rex Coleman is building at the intersection of AI security and ML systems engineering. He spent over a decade at FireEye and Mandiant in data analytics and enterprise sales, working with security teams across Fortune 500 organizations. He is completing his MS in Computer Science at Georgia Tech (Machine Learning specialization), where he researches AI security — adversarial evaluation of ML systems, agent exploitation, and ML governance tooling. He is the creator of govML, an open-source governance framework for ML research projects. CFA charterholder.

## Outline

1. **The Problem** (3 min): Multi-agent systems are the new default. No security testing framework exists. One compromised agent → what happens?
2. **The Framework** (3 min): Simulation-based testbed. Trust models, topologies, attacker types. Design for 8/10 (Gate 0.5).
3. **The Results** (10 min): E2 (zero-trust = only defense), E4 (adaptive adversary recovers 54%). Figures and confidence intervals.
4. **The Negative Results** (5 min): 4/6 hypotheses refuted. Topology, agent type, memory don't matter. Why this narrows the solution space.
5. **Implications** (3 min): Implement zero-trust now. Defense-in-depth against adaptive adversaries. What the agent economy needs.
6. **Demo / Q&A** (5 min): Framework walkthrough. govML governance. Reproducibility.
