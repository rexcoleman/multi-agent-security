# METRICS CONTRACT — FP-15 Multi-Agent Security

## Primary Metrics

| Metric | Definition | Range | Higher = |
|--------|-----------|-------|----------|
| **Cascade rate** | Fraction of agents in COMPROMISED state at simulation end | [0, 1] | Worse (more agents compromised) |
| **Poison rate** | Fraction of total decisions that are poisoned | [0, 1] | Worse (more decisions corrupted) |

## Secondary Metrics

| Metric | Definition | Used In |
|--------|-----------|---------|
| Tasks delegated | Total inter-agent task delegations | All experiments |
| Tasks filtered | Tasks where trust model cleaned poison | E2 (trust model) |
| Cascade over time | Per-timestep cascade rate | Mechanism analysis |
| Inflection step | First timestep where cascade > 50% | Mechanism analysis |

## Aggregation

- **Across seeds:** mean +/- std (5 seeds: 42, 123, 456, 789, 1024)
- **Statistical test:** Bootstrap CI (95%), 10K resamples
- **Multiple comparisons:** Bonferroni correction for pairwise trust model comparisons
- **Effect size threshold:** ≥10pp cascade/poison rate difference for practitioner significance

## Reporting Standard

All results in FINDINGS.md include: metric name, aggregation (mean), dispersion (std), sample size (5 seeds), evidence tag ([DEMONSTRATED] for 5-seed results).
