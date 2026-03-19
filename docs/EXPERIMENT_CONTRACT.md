# EXPERIMENT CONTRACT — FP-15 Multi-Agent Security

## 0) Gate 0.5 Cross-Reference

**EXPERIMENTAL_DESIGN.md status:** PASS (lock_commit: `82d4a63`)

### Comparison Baselines (from EXPERIMENTAL_DESIGN.md §3)

| # | Published Method | Implementation |
|---|-----------------|----------------|
| 1 | OWASP LLM Top 10 v2 | Coverage overlap analysis |
| 2 | FP-02 single-agent baseline | Same attacks, single vs multi-agent delta |
| 3 | ACM Computing Surveys taxonomy | Empirical validation of theoretical categories |

### Ablation Plan (from EXPERIMENTAL_DESIGN.md §5)

| Component | Hypothesis | Verified? |
|-----------|-----------|-----------|
| Inter-agent trust | Implicit = max cascade | YES (E2) |
| Capability scoping | Reduces cascade partially | YES (E2) |
| Agent authentication | Without auth, spoofing 100% | PARTIALLY (E4) |
| Orchestrator oversight | Without oversight, no quality check | NOT TESTED (deferred) |
| Shared memory | Accelerates cascade | REFUTED (E6: 1.2pp diff) |

## 1) Experiment Matrix

| ID | IV | Levels | DV | Seeds |
|----|-----|--------|----|-------|
| E1 | Agent count | 2,3,5,7,10 | Cascade rate, poison rate | 5 |
| E2 | Trust model | implicit, capability, zero-trust | Cascade rate, poison rate | 5 |
| E3 | Topology | hierarchical, flat, star | Cascade rate, poison rate | 5 |
| E4 | Attacker type | naive, defense-aware, credential | Cascade rate, poison rate | 5 |
| E5 | Agent composition | 4 mixes | Cascade rate, poison rate | 5 |
| E6 | Memory mode | shared, partitioned, isolated | Cascade rate, poison rate | 5 |
| S1 | Base cascade prob | 0.05-0.50 | E2 robustness | 5 |
| S2 | Base cascade prob | 0.05-0.50 | E4 robustness | 5 |
| S3 | Verification prob | 0.0-1.0 | Threshold analysis | 5 |

## 2) Phase 1 Completion Verification

| # | Check | Status |
|---|-------|--------|
| 1 | All 3 baselines run | [x] OWASP (conceptual), FP-02 (delta), ACM (coverage) |
| 2 | 5 seeds per experiment | [x] |
| 3 | All ablation components tested | [x] 4/5 (orchestrator oversight deferred — ADR-0003) |
| 4 | Ground truth used as planned | [x] Synthetic + FP-02 transfer |
| 5 | Deviations logged | [x] ADR-0001 (simulation), ADR-0002 (base_prob), ADR-0003 (CrewAI deferred) |
| 6 | All experiment outputs exist | [x] 6 experiments + sensitivity |
