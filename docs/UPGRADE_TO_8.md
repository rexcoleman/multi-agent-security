# FP-15 Upgrade Plan: 7.5 → 8/10

> **Date:** 2026-03-19
> **Current score:** 7.5/10
> **Gap:** Simulation-only. FP-16 proved sim-to-real gap is 48pp.
> **Target:** 8/10

---

## The Gap

FP-15's quantitative claims are undermined by FP-16's findings:

| FP-15 Claim | FP-16 Reality | Gap |
|-------------|--------------|-----|
| 97% poison under implicit trust | 49% poison | 48pp |
| Zero-trust cuts 40pp | Zero-trust cuts 6pp | 34pp |
| Topology doesn't matter | Unknown on real agents | Unvalidated |

FP-15's QUALITATIVE findings hold (zero-trust > implicit, topology is minor, agent type is minor). But the QUANTITATIVE results are misleading without real-agent validation.

---

## Option A: Run Real Agent Validation (~$5 API, ~30 min)

Reproduce FP-15's two most important experiments with real Claude Haiku agents:

| Experiment | What It Validates | API Calls | Est. Cost |
|-----------|-------------------|-----------|-----------|
| E2 (trust model) | Implicit vs capability vs zero-trust with real agents | ~150 | ~$2 |
| E3 (topology) | Hierarchical vs flat vs star with real agents | ~150 | ~$2 |

**What we'd report:**
- Side-by-side: simulation prediction vs real agent result for each condition
- Updated quantitative claims with real numbers
- Simulation model critique: what the model gets right (ordering) and wrong (magnitude)

**Effort:** Write real-agent runner for FP-15 (~1 hr code), run experiments (~30 min), update FINDINGS (~1 hr).

**This closes the gap because:** R34.7 requires sim-to-real validation for Tier 2. Adding it moves FP-15 from "simulation with acknowledged gap" to "simulation validated against real agents."

---

## Option B: Reframe as Simulation Methodology Paper

Instead of validating, explicitly position FP-15 as a simulation methodology contribution:

- **Rewrite novelty claim:** "We propose a configurable simulation framework for multi-agent cascade analysis" (not "we measure cascade rates")
- **Add FP-16 validation as a section:** "Section 7: Simulation-to-Real Gap Analysis" incorporating FP-16's findings directly
- **Contribution becomes:** the FRAMEWORK + the gap analysis, not the quantitative predictions

**Effort:** Rewrite FINDINGS framing (~2 hrs), add gap analysis section (~1 hr).

**This works because:** The framework IS useful — FP-16 used it as the starting point. The contribution shifts from "these are the cascade rates" to "this is how to model cascade, and here's what the model gets right and wrong."

---

## Recommendation: Option A

Option A is faster (~2.5 hrs vs ~3 hrs), directly addresses R34.7, and produces stronger results. The side-by-side comparison (simulation vs real) is itself a novel finding.

**Implementation:**

1. Create `scripts/run_real_agents.py` — runs E2 and E3 with real Claude Haiku
2. Run via nohup (~$5, ~30 min)
3. Add "Real Agent Validation" section to FINDINGS.md
4. Update blog draft with validation results
5. Re-run check_all_gates.sh

**After this, FP-15 has:**
- Simulation results (existing) + real agent validation (new)
- Parameter sensitivity (Track A, done)
- Mechanism analysis (Track A, done)
- Honest gap analysis between simulation and reality
- Complete content pipeline (existing)

**Score: 8/10** — simulation framework + real validation + sensitivity + mechanism + honest gap analysis.
