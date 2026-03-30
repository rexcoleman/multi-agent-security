# HYPOTHESIS REGISTRY — FP-15 Multi-Agent Security

> **Project:** FP-15 (Multi-Agent Security Testing Framework)
> **Created:** 2026-03-19
> **Status:** Pre-registered (6/6 hypotheses locked before Phase 1)
> **Lock commit:** `82d4a63`
> **Lock date:** 2026-03-19

> **Temporal gate (LL-74):** All hypotheses committed and locked before any experimental results are generated.

---

## H-1: Cascade rate is super-linear with agent count

| Field | Value |
|-------|-------|
| **Statement** | Under implicit trust, the fraction of compromised agents after 20 time steps increases super-linearly with agent count (i.e., cascade rate at N=10 > 2x cascade rate at N=5). |
| **Prediction** | cascade_rate(10) / cascade_rate(5) > 2.0 |
| **Status** | PENDING |
| **Evidence** | E1 results |
| **Linked Experiment** | E1: Cascade vs Agent Count |
| **lock_commit** | `82d4a63` |

---

## H-2: Zero-trust reduces cascade by ≥50% vs implicit trust

| Field | Value |
|-------|-------|
| **Statement** | Zero-trust architecture reduces cascade propagation rate by at least 50% compared to implicit trust, holding agent count and topology constant at 5 agents, hierarchical. |
| **Prediction** | cascade_rate(zero_trust) ≤ 0.5 * cascade_rate(implicit) |
| **Status** | PENDING |
| **Evidence** | E2 results |
| **Linked Experiment** | E2: Trust Model Comparison |
| **lock_commit** | `82d4a63` |

---

## H-3: Flat topology has higher cascade rate than hierarchical

| Field | Value |
|-------|-------|
| **Statement** | All-to-all (flat) topology produces higher cascade rate than hierarchical (tree) topology because every agent is directly reachable from every other agent. |
| **Prediction** | cascade_rate(flat) > cascade_rate(hierarchical) |
| **Status** | PENDING |
| **Evidence** | E3 results |
| **Linked Experiment** | E3: Topology Comparison |
| **lock_commit** | `82d4a63` |

---

## H-4: Adaptive adversary partially defeats zero-trust

| Field | Value |
|-------|-------|
| **Statement** | A defense-aware attacker achieves higher cascade rate against zero-trust than a naive attacker, and a credential-theft attacker achieves the highest cascade rate of all three attacker types. |
| **Prediction** | cascade_rate(credential) > cascade_rate(defense_aware) > cascade_rate(naive) |
| **Status** | PENDING |
| **Evidence** | E4 results |
| **Linked Experiment** | E4: Adaptive Adversary |
| **lock_commit** | `82d4a63` |

---

## H-5: RL agents amplify cascade vs all-LLM systems

| Field | Value |
|-------|-------|
| **Statement** | Systems containing RL agents have higher cascade rates than all-LLM systems because RL agents are more susceptible to observation manipulation (FP-12 finding). |
| **Prediction** | cascade_rate(mixed_rl) > cascade_rate(all_llm) |
| **Status** | PENDING |
| **Evidence** | E5 results |
| **Linked Experiment** | E5: Mixed Agent Types |
| **lock_commit** | `82d4a63` |

---

## H-6: Shared memory accelerates cascade vs isolated memory

| Field | Value |
|-------|-------|
| **Statement** | Shared memory between agents accelerates cascade propagation because poisoned context persists and is read by all agents. Isolated memory reduces cascade by ≥30%. |
| **Prediction** | cascade_rate(isolated) ≤ 0.7 * cascade_rate(shared) |
| **Status** | PENDING |
| **Evidence** | E6 results |
| **Linked Experiment** | E6: Memory Ablation |
| **lock_commit** | `82d4a63` |

---

## H-7: Two-of-three constraint reduces cascade vs implicit trust

| Field | Value |
|-------|-------|
| **Statement** | The two-of-three capability constraint (each agent holds at most 2 of 3 capability categories: data_access, code_execution, external_communication) reduces cascade propagation rate compared to implicit trust, across all topologies and agent counts tested. |
| **Prediction** | poison_rate(two_of_three) < poison_rate(implicit) for all topology × agent_count combinations |
| **Status** | PENDING |
| **Evidence** | E7 results |
| **Linked Experiment** | E7: Two-of-Three Constraint |
| **lock_commit** | `358dba1` |

---

## H-8: Two-of-three performs between implicit and zero-trust

| Field | Value |
|-------|-------|
| **Statement** | The two-of-three constraint produces cascade rates between implicit trust (worst) and zero-trust (best) — it is a less restrictive but less effective defense than zero-trust. |
| **Prediction** | poison_rate(zero_trust) ≤ poison_rate(two_of_three) ≤ poison_rate(implicit) |
| **Status** | PENDING |
| **Evidence** | E7 results |
| **Linked Experiment** | E7: Two-of-Three Constraint |
| **lock_commit** | `358dba1` |

---

## H-9: Trust model effectiveness is topology-independent

| Field | Value |
|-------|-------|
| **Statement** | The relative ordering of trust models (zero-trust > two-of-three > capability-scoped > implicit) is consistent across all three topologies (hierarchical, flat, star). |
| **Prediction** | Ordering is identical for all topologies |
| **Status** | PENDING |
| **Evidence** | E7 results |
| **Linked Experiment** | E7: Two-of-Three Constraint |
| **Surprise detection** | If ordering DIFFERS by topology, that's a novel finding — topology × trust model interaction. |
| **lock_commit** | `358dba1` |

---

## H-10: Two-of-three advantage scales with agent count

| Field | Value |
|-------|-------|
| **Statement** | The cascade reduction advantage of two-of-three vs implicit trust increases with agent count (because more agents = more capability partitioning = more structural containment). |
| **Prediction** | (implicit_poison - two_of_three_poison) increases monotonically from n=5 to n=50 |
| **Status** | PENDING |
| **Evidence** | E7 results |
| **Linked Experiment** | E7: Two-of-Three Constraint |
| **lock_commit** | `358dba1` |

---

## Summary

| ID | Statement (short) | Prediction | Status |
|----|-------------------|-----------|--------|
| H-1 | Super-linear cascade with agent count | rate(10) > 2x rate(5) | REFUTED |
| H-2 | Zero-trust ≥50% cascade reduction | rate(ZT) ≤ 0.5 * rate(implicit) | PARTIALLY SUPPORTED |
| H-3 | Flat topology > hierarchical cascade | rate(flat) > rate(hierarchical) | SUPPORTED (real agents) |
| H-4 | Adaptive adversary defeats zero-trust | credential > defense_aware > naive | PARTIALLY SUPPORTED |
| H-5 | RL agents amplify cascade | rate(mixed_rl) > rate(all_llm) | REFUTED |
| H-6 | Shared memory accelerates cascade | rate(isolated) ≤ 0.7 * rate(shared) | REFUTED |
| H-7 | Two-of-three reduces cascade vs implicit | poison(2of3) < poison(implicit) for all conditions | PENDING |
| H-8 | Two-of-three between implicit and zero-trust | zero-trust ≤ 2of3 ≤ implicit | PENDING |
| H-9 | Trust model ordering is topology-independent | Same ordering all topologies | PENDING |
| H-10 | Two-of-three advantage scales with count | Gap increases n=5→50 | PENDING |
| H-11 | Capability assignment strategy doesn't matter | round-robin ≈ random ≈ clustered | PENDING |
| H-12 | Constraint-aware adversary partially defeats two-of-three | Recovers 30-50% of constraint advantage | PENDING |
