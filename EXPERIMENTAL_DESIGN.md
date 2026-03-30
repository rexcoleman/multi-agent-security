# Experimental Design Review — FP-15: Multi-Agent Security Testing Framework

> **Gate:** 0.5 (must pass before Phase 1 compute)
> **Date:** 2026-03-19
> **Target venue:** AISec Workshop (ACM CCS 2026) — Tier 2
> **lock_commit:** `82d4a63`
> **Designed for:** 8/10 from day 1 (Gate 0.5 + R34 depth escalation)

---

## 1) Project Identity

**Project:** FP-15 — Multi-Agent Security Testing Framework
**Target venue:** AISec Workshop (ACM CCS 2026), Tier 2
**Compute budget:** ~30-50 CPU-hours (Azure VM 2 vCPU), no GPU required
**Framework:** CrewAI + custom harness (LangGraph as secondary)
**LLM backend:** Claude API (Haiku for agents, Sonnet for orchestrator) + local Llama 3.1 8B fallback

---

## 2) Novelty Claim (one sentence)

> First open-source framework quantifying how single-agent compromise cascades through multi-agent systems, with empirical comparison of zero-trust vs implicit-trust defense architectures.

**Self-test (≤25 words):** We measure compromise propagation rates in multi-agent systems and show zero-trust architectures reduce cascade spread by N% vs implicit trust. ✓

---

## 3) Comparison Baselines

| # | Method | Citation | How We Compare | Why This Baseline |
|---|--------|----------|---------------|-------------------|
| 1 | OWASP LLM Top 10 v2 | OWASP Foundation, 2025 | Our attack taxonomy extends OWASP with 3 multi-agent-specific classes (delegation abuse, cascade poisoning, identity spoofing). Report coverage overlap and novel classes. | Industry standard threat enumeration. Reviewer expects positioning against it. |
| 2 | FP-02 single-agent baseline | Coleman, 2026 (own work) | Run identical FP-02 attacks on single agent, then same attacks on multi-agent system. Delta = cascade amplification factor. | Controls for multi-agent novelty. Without this, reviewer says "this is just FP-02 with more agents." |
| 3 | ACM Computing Surveys agent threat taxonomy | Masterman et al., 2025 | Their taxonomy is theoretical. We provide empirical validation: which of their threat categories actually manifest in a real multi-agent testbed, and at what rates? | Most comprehensive published survey. Reviewer will ask how we relate. |

---

## 4) Pre-Registered Reviewer Kill Shots

| # | Criticism | Planned Mitigation | Design Decision |
|---|----------|-------------------|-----------------|
| 1 | "This is just FP-02 with more agents — where's the new attack surface?" | Experiment 1 explicitly measures cascade amplification: same attack on 1 agent vs same attack propagated through 2, 5, 10 agents. Show that compromise rate is super-linear (not just N copies of single-agent risk). | Run single-agent baseline as control condition in every experiment. |
| 2 | "CrewAI/LangGraph are toy frameworks, not production systems." | Test on both CrewAI AND custom multi-agent harness. Show attacks generalize across frameworks. Reference real-world multi-agent deployments (Solana trading agents, DeFi bots, enterprise automation). | Two frameworks minimum. Include custom harness to prove framework-independence. |
| 3 | "87% cascade figure is from Galileo — you're just replicating their work." | Galileo's 87% was observational (one case study, one system). We provide controlled experiments across 3 network topologies, 3 trust models, and 3 agent counts with 5 seeds. Our contribution is the systematic framework, not the number. | Design experiments to VARY cascade rate by topology and trust model, not just confirm one number. |
| 4 | "No formal model — this is just empirical." | Provide a graph-based propagation model (infection probability per edge, trust weight per connection) that predicts cascade rates. Validate predictions against empirical results. The model is simple but falsifiable. | Include lightweight formal model in Phase 0 design. |

---

## 5) Ablation Plan

| Component / Feature | Hypothesis When Removed | Expected Effect | Priority |
|---------------------|------------------------|-----------------|----------|
| Inter-agent trust (set all trust = 1.0) | Implicit trust baseline: maximum cascade propagation | Fastest spread, highest downstream poisoning rate | HIGH — this is the control |
| Per-agent capability scoping | Removing capability limits lets compromised agent access all tools | Propagation rate increases; tool-based attacks become possible | HIGH |
| Agent authentication (identity verification) | Without auth, any agent can impersonate any other | Identity spoofing attacks succeed at ~100% | HIGH |
| Orchestrator oversight (Ralph loop pattern) | Without oversight agent, no quality check on delegated tasks | Poisoned outputs pass through unchecked | MEDIUM |
| Shared context/memory | Without shared memory, agents operate independently | Cascade rate should drop dramatically (isolation test) | MEDIUM — mechanism test |

---

## 6) Ground Truth Audit

| Source | Type | Estimated Count | Known Lag | Estimated Positive Rate | Limitations |
|--------|------|----------------|-----------|------------------------|-------------|
| Controlled injection (our testbed) | Synthetic ground truth | ~500-1000 test cases per experiment | None (synthetic) | Controlled: 0%, 10%, 25%, 50% compromise rates | Synthetic may not reflect real-world agent behavior |
| FP-02 attack success rates | Empirical transfer | 19 scenarios, 3 seeds | Tested on Claude Sonnet only | 25-100% by attack class | Single LLM backend, single framework |

### Alternative Sources Considered

| Source | Included? | Rationale |
|--------|-----------|-----------|
| Real-world multi-agent incident reports | NO (not enough public data) | <10 documented incidents as of 2026. Insufficient for statistical analysis. Referenced qualitatively. |
| Galileo AI cascade study | YES (qualitative) | Provides the 87%/4hr benchmark. We reproduce the SCENARIO, not the data. |
| NIST Agentic Control Overlays | NO (not yet published) | In draft. Will reference when available. |

---

## 7) Statistical Plan

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Seeds | 5 (42, 123, 456, 789, 1024) | govML standard. Captures LLM stochasticity. |
| Significance test | Bootstrap CI (95%) | Non-parametric; no distributional assumptions on agent behavior. |
| Effect size threshold | ≥10pp cascade rate difference between trust models | Practitioner-meaningful: <10pp is too small to justify architecture change. |
| CI method | Percentile bootstrap, 10K resamples | Standard for small-N experiments with unknown distributions. |
| Multiple comparison correction | Bonferroni for pairwise trust model comparisons | 3 trust models = 3 pairwise comparisons. |

---

## 8) Related Work Checklist (≥5 for Tier 2)

| # | Paper | Year | Relevance | How We Differ |
|---|-------|------|-----------|---------------|
| 1 | Masterman et al. — "Landscape of Emerging AI Agent Architectures" | 2024 | Comprehensive agent architecture taxonomy | They enumerate architectures; we test them under adversarial conditions |
| 2 | Tian et al. — "Evil Geniuses: Delving into the Safety of LLM-based Agents" | 2024 | Multi-agent safety evaluation | Focus on jailbreaking multi-agent chat; we focus on cascade compromise in task-delegation systems |
| 3 | Cohen et al. — "Here Comes the AI Worm" | 2024 | Self-replicating adversarial inputs across agents | Demonstrates agent-to-agent propagation of adversarial inputs; we quantify propagation RATES across architectures |
| 4 | Gu et al. — "Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents" | 2024 | Shows one poisoned input can compromise many agents | Focuses on shared input channel; we focus on delegation-based cascade (different propagation mechanism) |
| 5 | Xi et al. — "Rise and Potential of Large Language Model Based Agents: A Survey" | 2023 | Foundational LLM agent survey | Broad survey; we provide focused security testing framework |
| 6 | Coleman — FP-02: Agent Red-Team Framework | 2026 | Single-agent attack baseline (7 classes) | We extend from single-agent to multi-agent cascade; FP-02 is our control condition |
| 7 | Coleman — FP-12: RL Agent Vulnerability | 2026 | RL policy attacks (observation > reward asymmetry) | We test whether RL-trained agents in multi-agent systems amplify cascade risk |

---

## 9) Design Review Checklist (Gate 0.5)

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 1 | Novelty claim stated in ≤25 words | [x] | §2 |
| 2 | ≥2 comparison baselines identified | [x] | §3: OWASP, FP-02 single-agent, ACM survey |
| 3 | ≥2 reviewer kill shots with mitigations | [x] | §4: 4 kill shots |
| 4 | Ablation plan with hypothesized effects | [x] | §5: 5 components |
| 5 | Ground truth audit: sources, lag, positive rate | [x] | §6: synthetic + FP-02 transfer |
| 6 | Alternative label sources considered | [x] | §6: incidents, Galileo, NIST |
| 7 | Statistical plan: seeds, tests, CIs | [x] | §7: 5 seeds, bootstrap, Bonferroni |
| 8 | Related work: ≥5 papers | [x] | §8: 7 papers |
| 9 | Hypotheses pre-registered in HYPOTHESIS_REGISTRY | [ ] | To create before Phase 1 |
| 10 | lock_commit set in HYPOTHESIS_REGISTRY | [ ] | To set before Phase 1 |
| 11 | Target venue identified | [x] | AISec Workshop (ACM CCS 2026) |
| 12 | This document committed before any training script | [x] | This commit |

**Gate 0.5 verdict:** [x] PASS (pending items 9-10 before Phase 1 start)

---

## 10) Tier 2 Depth Escalation (R34)

### Depth Commitment

**Primary finding (one sentence):** Single-agent compromise cascades super-linearly through multi-agent systems under implicit trust, and zero-trust architectures reduce cascade propagation by ≥50%.

**Evaluation settings (minimum 2):**

| # | Setting | How It Differs | What It Tests |
|---|---------|---------------|---------------|
| 1 | CrewAI task-delegation system (3, 5, 10 agents) | Primary framework, hierarchical delegation | Core cascade propagation rates |
| 2 | Custom flat-topology multi-agent harness | No hierarchy, all-to-all communication | Whether hierarchy is protective or cascade-amplifying |
| 3 | Mixed RL + LLM agent system | Includes FP-12-style RL agent alongside LLM agents | Whether RL agents amplify or dampen cascade |

### Mechanism Analysis Plan

| Finding | Proposed Mechanism | Experiment to Verify |
|---------|-------------------|---------------------|
| Cascade rate is super-linear with agent count | Trust transitivity: Agent B trusts Agent A's output, so Agent C trusts it too (transitive closure) | Compare cascade under transitive trust (default) vs per-hop trust verification |
| Zero-trust reduces cascade by ≥50% | Each agent independently validates inputs, breaking transitive trust chains | Ablation: toggle zero-trust per agent and measure marginal cascade reduction |
| Shared memory accelerates cascade | Poisoned context persists and is read by all agents | Ablation: remove shared memory, measure cascade rate with isolated agent contexts |

### Adaptive Adversary Plan

| Robustness Claim | Weak Test (baseline) | Adaptive Test (attacker knows defense) |
|-----------------|---------------------|---------------------------------------|
| Zero-trust reduces cascade | Static attacker: same FP-02 attacks regardless of defense | Adaptive attacker: modifies attack to mimic legitimate delegation patterns, uses valid agent IDs, crafts outputs that pass zero-trust validation checks |
| Identity verification prevents spoofing | Naive spoofing: attacker uses wrong agent name | Adaptive spoofing: attacker compromises one agent's credentials and delegates as that agent |

### Formal Contribution Statement (draft)

We contribute:
1. **An open-source multi-agent security testing framework** with configurable trust models, agent topologies, and attack injection points
2. **Empirical cascade propagation rates** across 3 agent counts × 3 trust models × 2 frameworks × 5 seeds, showing that implicit trust amplifies single-agent compromise super-linearly
3. **Comparative defense analysis** demonstrating that zero-trust architectures reduce cascade propagation by ≥50% but at measurable latency cost, providing practitioners with a quantified security-performance tradeoff

### Published Baseline Reproduction Plan

| Published Method | Their Benchmark | Our Reproduction Plan |
|-----------------|----------------|----------------------|
| FP-02 single-agent attacks (Coleman 2026) | 19 scenarios, 3 seeds, Claude Sonnet | Reproduce top 3 attack classes on same Claude backend in single-agent mode. Then inject same attacks into multi-agent system. Delta = cascade amplification. |
| Cohen et al. "AI Worm" propagation | GenAI ecosystem simulation | Reproduce their propagation scenario in our testbed: one poisoned agent, measure downstream impact over time. Compare their qualitative findings to our quantitative rates. |

### Threats to Validity

**Internal validity:**
- Simulation uses fixed cascade probability (0.15) — sensitivity analysis (§ Parameter Sensitivity) shows results are robust across 0.05-0.50.
- Two-of-three capability assignment is round-robin — random assignment may produce different results (ablation planned but not yet run).
- Adaptive adversary (E4) only tested against original 3 trust models, not yet against two-of-three.

**External validity:**
- Simulation overestimates cascade by 37pp vs real Claude Haiku agents (§ Real Agent Validation). SE-150 results carry same synthetic qualifier.
- Single LLM backend (Haiku) for real validation. Other models (GPT-4, Llama) may show different cascade dynamics.
- Agent counts up to 50 tested. Production systems with 100+ agents may exhibit different dynamics.

**Construct validity:**
- "Cascade rate" measures fraction of agents compromised, not severity of compromise. A 50% cascade rate where compromised agents produce low-quality-but-harmless output differs from 50% cascade with data exfiltration.
- "Capability partitioning" in simulation is binary (has/doesn't have). Real capability enforcement may be partial or bypassable.

### Depth Escalation Checklist

| # | Requirement | Status |
|---|------------|--------|
| 1 | ONE primary finding identified | [x] | Super-linear cascade under implicit trust |
| 2 | ≥2 evaluation settings designed | [x] | CrewAI hierarchical, custom flat, mixed RL+LLM |
| 3 | Mechanism analysis planned for each major claim | [x] | Trust transitivity, shared memory, per-hop verification |
| 4 | Adaptive adversary test planned | [x] | Attacker mimics legitimate delegation, credential theft |
| 5 | Formal contribution statement drafted | [x] | 3 contributions |
| 6 | ≥1 published baseline reproduction planned | [x] | FP-02 single-agent, Cohen et al. AI Worm |

---

## 11) Experiment Matrix

| Experiment | Independent Variable | Levels | Dependent Variable | Seeds |
|-----------|---------------------|--------|-------------------|-------|
| E1: Cascade vs agent count | Number of agents | 2, 5, 10 | % downstream decisions poisoned at t=1hr | 5 |
| E2: Trust model comparison | Trust architecture | Implicit, capability-scoped, zero-trust | Cascade propagation rate | 5 |
| E3: Topology comparison | Network structure | Hierarchical (CrewAI), flat (custom), star | Time to N% cascade | 5 |
| E4: Adaptive adversary | Attacker knowledge | None, defense-aware, credential-theft | Attack success rate under zero-trust | 5 |
| E5: Mixed agent types | Agent composition | All-LLM, LLM+RL, LLM+rule-based | Cascade rate by agent type | 5 |
| E6: Shared memory ablation | Memory isolation | Shared, partitioned, isolated | Cascade rate | 5 |

| E7: Two-of-three constraint | Trust architecture | Implicit, capability-scoped, zero-trust, two-of-three | Cascade rate, poison rate | 5 |

**Total runs:** 7 experiments. E1-E6: ~150 runs. E7: 4 models × 4 agent counts × 3 topologies × 5 seeds = 240 runs.
**Estimated compute:** ~30-50 CPU-hours (API calls are the bottleneck, not compute)

---

## 8a) Novelty Plan (SE-150: Two-of-Three Constraint)

> [SEED: sunset after 5 projects if this never changes experimental design | PT-5]

**Prior art search strategy:** Google Scholar + arXiv for "capability-based security multi-agent", "least privilege agent systems", "NVIDIA NemoClaw security", "two-of-three constraint". Minimum 5 papers reviewed.
**Expected contribution type:** Novel combination — importing capability-based security (Saltzer & Schroeder 1975, OS security) into multi-agent LLM systems.
**What result would surprise us?**
- EXPECTED: Two-of-three performs between zero-trust and implicit trust.
- SURPRISE 1: Two-of-three OUTPERFORMS zero-trust for some topology (less restrictive but more effective?)
- SURPRISE 2: Two-of-three is WORSE than implicit for some topology (constraint creates attack surface?)
- SURPRISE 3: Non-monotonic cascade dynamics with agent count under two-of-three (emergent behavior)
- SURPRISE 4: Topology × trust model interaction — same model behaves differently across topologies

| Novel Component | How Tested (ablation) | Expected Effect If Removed |
|----------------|----------------------|---------------------------|
| Two-of-three capability constraint | Remove constraint → agents get all 3 capabilities (= implicit) | Cascade rate increases to implicit baseline |
| Capability-based acceptance filter | Replace with implicit acceptance | Poison rate increases (no capability overlap check) |
| Round-robin capability assignment | Replace with random assignment | May change topology × trust interaction if capability distribution matters |

---

## 8b) Impact Plan (SE-150)

> [SEED: sunset after 5 projects if this never produces a shipped artifact | PT-5]

**Target practitioners:** Multi-agent system builders using CrewAI, LangChain, AutoGen. Estimated ~50K+ active developers.
**Planned artifacts:**
- TwoOfThreeConstraint class in src/trust.py (importable, documented)
- Comparison table: zero-trust vs two-of-three tradeoffs for practitioners
- Architecture recommendation: which trust model for which topology
**Deployment path:** `pip install` or copy trust.py into existing multi-agent project. Drop-in replacement for existing trust model.

---

## 8c) Generalization Plan (SE-150)

> [SEED: sunset after 5 projects if this doesn't improve generalization scores | PT-5]

**Evaluation conditions (target ≥2 for Tier 2+):**

| Condition | Why This Tests Generalization | Data/Setup Required |
|-----------|------------------------------|-------------------|
| 3 topologies (hierarchical, flat, star) | Tests whether constraint effectiveness depends on communication structure | Existing topology implementations |
| 4 agent counts (5, 10, 20, 50) | Tests scaling behavior — does constraint hold at larger systems? | Parameterized simulation |
| 4 trust models compared side-by-side | Establishes relative positioning across defense strategies | All trust models in trust.py |

**What constitutes transfer evidence:** Two-of-three should reduce cascade relative to implicit trust across ALL topologies and agent counts. If it fails on any topology, that's a boundary condition to document.

---

## E7d-E7f: Missing Experiments (identified by govML-driven design review)

> These experiments were identified by running the govML pipeline AFTER E7a-c, revealing conditions that governance-first design would have required upfront. Running them now to close the gaps.

### E7d: Capability Assignment Ablation

**Question:** Does the round-robin assignment of capabilities matter, or would random assignment produce equivalent results?

| Assignment Strategy | Description | What It Tests |
|---|---|---|
| Round-robin (current) | Agent i gets combo [i % 3] | Deterministic, maximally distributed |
| Random | Each agent gets a random 2-of-3 combo | Whether structural distribution matters vs random partitioning |
| Clustered | First N/3 agents get combo 0, next N/3 get combo 1, rest get combo 2 | Whether geographic clustering of capabilities affects cascade |

**Prediction:** Round-robin ≈ random (partition distribution shouldn't matter if combos are equal probability). Clustered may differ if topology creates capability-homogeneous neighborhoods.

### E7e: Adaptive Adversary vs Two-of-Three

**Question:** Can an adversary who knows the two-of-three constraint exploit it? E4 only tested adversaries against the original 3 trust models.

| Adversary Type | Strategy Against Two-of-Three |
|---|---|
| Naive | Standard attack, unaware of capability constraints |
| Constraint-aware | Targets agents with data_access + external_communication combo (the exfiltration-capable pair). Focuses cascade on agents whose 2-of-3 permits the most dangerous action. |

**Prediction:** Constraint-aware attacker will partially defeat two-of-three by targeting the weakest capability combination, recovering 30-50% of the constraint's advantage (similar to E4 adaptive vs zero-trust recovery of 54%).

### E7f: Power Analysis

**Question:** Are 5 seeds sufficient for the effect sizes observed in E7a-c?

**Method:** For each key comparison, compute the 95% CI width and compare to effect size. If CI width > 50% of effect size, 5 seeds is insufficient for that comparison.

---

## 12) Phase Plan

| Phase | Activities | Gate | Compute |
|-------|-----------|------|---------|
| 0 | Contracts, HYPOTHESIS_REGISTRY, testbed scaffold, data contracts | Gate 0.5 (this doc) | 0 |
| 1 | Build testbed (CrewAI + custom), implement attacks, run E1-E3 | Gate 3 (experiment fields) | ~20 CPU-hrs |
| 2 | Run E4-E6 (adaptive adversary, mixed agents, memory ablation) | Gate 4 (analysis) | ~15 CPU-hrs |
| 3 | FINDINGS.md, figures, statistical tests, blog draft | Gate 6 (publication) | ~5 CPU-hrs |
| 4 | Conference abstract, distribution, Gate 9 | Gate 9 (V-cluster) | 0 |
