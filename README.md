# Simulation Overestimates Multi-Agent Cascade by 37pp — But Topology Matters More Than We Thought

**Zero-trust cuts cascade by ~7pp (not 40pp). Topology DOES matter — hierarchical is protective (0.560 vs flat 0.733). The simulation overestimates severity by 37pp but correctly predicts zero-trust is best.**

**Blog post:** [Our Simulation Was Wrong by 37 Percentage Points](https://rexcoleman.dev/posts/multi-agent-security/)

![govML](https://img.shields.io/badge/govML-v3.3-blue) ![Quality](https://img.shields.io/badge/quality-8.3-brightgreen) ![License](https://img.shields.io/badge/license-MIT-green)

![Key Result](outputs/figures/e1_cascade_vs_count.png)

## Key Results

| Agent Count | Cascade Rate (mean +/- std) | Poison Rate (mean +/- std) |
|------------|---------------------------|---------------------------|
| 2 | 1.000 +/- 0.000 | 0.945 +/- 0.006 |
| 3 | 1.000 +/- 0.000 | 0.960 +/- 0.011 |
| 5 | 1.000 +/- 0.000 | 0.974 +/- 0.009 |
| 7 | 1.000 +/- 0.000 | 0.981 +/- 0.008 |
| 10 | 1.000 +/- 0.000 | 0.978 +/- 0.006 |

**Core insight:** Zero-trust cuts cascade by ~7pp (not 40pp). Topology DOES matter — hierarchical is protective (0.560 vs flat 0.733). The simulation overestimates severity by 37pp but correctly predicts zero-trust is best.

## Quick Start

```bash
git clone https://github.com/rexcoleman/multi-agent-security
cd multi-agent-security
pip install -e .
bash reproduce.sh
```

## Project Structure

```
FINDINGS.md # Research findings with pre-registered hypotheses and full results
EXPERIMENTAL_DESIGN.md # Pre-registered experimental design and methodology
HYPOTHESIS_REGISTRY.md # Hypothesis predictions, results, and verdicts
reproduce.sh # One-command reproduction of all experiments
governance.yaml # govML governance configuration
CITATION.cff # Citation metadata
LICENSE # MIT License
pyproject.toml # Python project configuration
scripts/ # Experiment and analysis scripts
src/ # Source code
tests/ # Test suite
outputs/ # Experiment outputs and results
data/ # Data files and datasets
config/ # Configuration files
docs/ # Documentation and decision records
```

## Methodology

See [FINDINGS.md](FINDINGS.md) and [EXPERIMENTAL_DESIGN.md](EXPERIMENTAL_DESIGN.md) for detailed methodology, pre-registered hypotheses, and full experimental results with multi-seed validation.

## Limitations

- **Simulation-based, not real LLM agents — and showed the gap is 48pp.** real agent experiments found 49% poison rate where this simulation predicted 97%. The simulation overestimates cascade severity because real agents have inherent semantic resistance. Qualitative findings (zero-trust > implicit) hold but quantitative predictions do not transfer. See FINDINGS for the simulation-to-real gap analysis.
- **Fixed cascade probability.** The base cascade probability (0.15) was tuned for differentiation. Real-world cascade probability depends on LLM capability, prompt design, and task complexity. We report relative comparisons between conditions, not absolute rates.
- **No real-time threat intelligence.** The simulation doesn't model evolving threats, model updates, or adversary learning over multiple encounters. Each run is a static snapshot.
- **5 agents maximum in most experiments.** E1 goes to 10 agents, but the primary results use 5. Larger systems (50-100 agents) may exhibit different cascade dynamics (e.g., partition effects, natural firebreaks).
- **Single compromised agent assumption.** All experiments start with exactly 1 compromised agent. Multi-point compromise (2+ initial attackers) may produce qualitatively different dynamics.

## Citation

If you use this work, please cite using the metadata in [CITATION.cff](CITATION.cff).

## License

[MIT](LICENSE) 2026 Rex Coleman

---

Governed by [govML](https://rexcoleman.dev/posts/govml-methodology/) v3.3
