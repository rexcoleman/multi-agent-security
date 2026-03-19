# DATA CONTRACT — FP-15 Multi-Agent Security

## 1) Purpose & Scope

Data governance for the Multi-Agent Security Testing Framework. Covers simulation configuration, ground truth definitions, and output artifacts.

## 1b) Ground Truth Audit (Gate 0.5)

### Label Sources

| Source | Type | Count | Known Lag | Positive Rate | Limitations |
|--------|------|-------|-----------|---------------|-------------|
| Controlled injection (testbed) | Synthetic | ~500-1000 per experiment | None | Controlled: 0-50% | Synthetic may not reflect real LLM behavior |
| FP-02 attack rates | Empirical transfer | 19 scenarios | Tested on Claude Sonnet only | 25-100% by class | Single LLM backend |

### Alternative Sources Considered

| Source | Included? | Rationale |
|--------|-----------|-----------|
| Real-world incidents | NO | <10 documented cases as of 2026 |
| Galileo AI cascade study | YES (qualitative) | Provides 87%/4hr benchmark |
| NIST Agentic Control Overlays | NO | Not yet published |

## 2) Canonical Data Paths

| Artifact | Path | Format |
|----------|------|--------|
| Experiment config | `config/base.yaml` | YAML |
| E1-E6 results | `outputs/experiments/e*_results.json` | JSON |
| Combined summary | `outputs/experiments/all_experiments_summary.json` | JSON |
| Sensitivity analysis | `outputs/experiments/sensitivity_analysis.json` | JSON |

## 3) Simulation Parameters

All parameters defined in `config/base.yaml`. No hardcoded values in scripts.

| Parameter | Default | Range Tested |
|-----------|---------|-------------|
| base_accuracy | 0.95 | Fixed |
| compromise_potency | 0.90 | Fixed |
| base_cascade_probability | 0.15 | 0.05-0.50 (sensitivity sweep) |
| verification_prob (zero-trust) | 0.80 | 0.0-1.0 (threshold sweep) |
| seeds | [42,123,456,789,1024] | Fixed |
| time_steps | 20 | Fixed |
