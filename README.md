# FP-15: Multi-Agent Security Testing Framework

Under implicit trust, a single compromised agent cascades to 100% of a multi-agent system with 97% poison rate. Zero-trust cuts poison by 40pp, but adaptive adversaries recover 54% of that advantage. The simulation-to-real gap is 37pp — real Claude agents resist at 60%, not 97%.

**Blog post:** [Our Simulation Was Wrong by 37 Percentage Points](https://rexcoleman.dev/posts/multi-agent-security/)

## Key Finding

Under implicit trust (the default in CrewAI, AutoGen, and most frameworks), a single compromised agent cascades to 100% of the system with 97% poison rate. **Zero-trust is the only effective defense**, cutting poison rate by 40pp — but adaptive adversaries recover 54% of that advantage.

## Quick Start

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v          # 16 tests
python scripts/run_experiments.py   # All 6 experiments × 5 seeds
python scripts/make_figures.py      # 7 publication figures
```

Or run everything:
```bash
bash reproduce.sh
```

## Experiments

| ID | Question | Key Finding |
|----|----------|-------------|
| E1 | Does cascade scale with agent count? | 100% cascade at ALL sizes (2-10 agents) |
| E2 | Which trust model defends best? | Zero-trust: 84% cascade, 58% poison (vs 100%/97%) |
| E3 | Does topology matter? | No. All topologies → 100% cascade |
| E4 | Can adaptive adversaries defeat zero-trust? | Defense-aware attacker recovers 54% of ZT gains |
| E5 | Do agent types matter? | No. LLM, RL, rule-based — identical dynamics |
| E6 | Does shared memory accelerate cascade? | Barely. 1.2pp difference |

## Designed for 8/10

This project uses [govML](https://github.com/rexcoleman/govML) Gate 0.5 (Experimental Design Review) + R34 (Tier 2 Depth Escalation):
- 6 pre-registered hypotheses (4 refuted, 1 supported, 1 partial)
- 3 comparison baselines (OWASP, FP-02, ACM Survey)
- 4 pre-registered reviewer kill shots with mitigations
- 5-component ablation plan
- 3 evaluation settings
- Mechanism analysis for each major claim
- Adaptive adversary testing

## Structure

```
├── EXPERIMENTAL_DESIGN.md    # Gate 0.5 design review (designed for 8/10)
├── FINDINGS.md               # Full results with hypothesis resolutions
├── HYPOTHESIS_REGISTRY.md    # 6 pre-registered hypotheses
├── src/                      # Simulation framework
│   ├── agent.py              # Agent model (LLM, RL, rule-based)
│   ├── trust.py              # Trust models (implicit, capability-scoped, zero-trust)
│   ├── network.py            # Network simulation engine
│   └── attacker.py           # Attacker models (naive, defense-aware, credential-theft)
├── scripts/
│   ├── run_experiments.py    # Run all 6 experiments
│   └── make_figures.py       # Generate 7 publication figures
├── tests/                    # 16 tests
├── config/base.yaml          # All experiment parameters
├── blog/                     # Content pipeline (draft, LinkedIn, Substack, conference)
└── docs/                     # Governance documents
```

## License

MIT
