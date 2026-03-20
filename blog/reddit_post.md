# I built a multi-agent security simulation then validated against real LLM agents — the simulation was wrong by 37 percentage points

I built a simulation-based testbed for multi-agent cascade poisoning, ran 6 experiments, then validated against real Claude Haiku agents. The simulation predicted 97% poison rate under implicit trust. Real agents showed 60%. And the simulation said topology doesn't matter — real agents proved it does (17pp spread between hierarchical and flat).

I tested three trust models (implicit, capability-scoped, zero-trust), three topologies (hierarchical, flat, star), and three attacker types (naive, defense-aware, credential-theft). Five seeds per experiment, 16 passing tests. The simulation-to-real gap was the main finding: real LLMs have enough semantic understanding to partially resist cascade, something probabilistic models completely miss.

Key results:

- **Zero-trust is the only trust model that actually reduces cascade** — cuts poison rate by 40pp in simulation, confirmed as best defense with real agents too
- **Capability-scoped trust barely helps** — only 7pp improvement over implicit trust, despite being more complex to implement
- **Adaptive adversaries recover 54% of the zero-trust defense** — a defense-aware attacker pushes poison from 58% back to 90% by crafting outputs that pass verification
- **Topology matters with real agents** — hierarchical (56% poison) outperforms flat (73%) by 17pp, but the simulation showed no difference
- **What you say matters more than who you are** — credential theft is less effective than an attacker who crafts convincing outputs

Methodology: simulation with configurable trust architectures and network topologies, validated against real Claude Haiku agents running in a multi-agent framework. 5 seeds per experiment. The qualitative finding (zero-trust > implicit) holds across both simulation and real agents, but the quantitative predictions are off by 37pp.

Repo: [github.com/rexcoleman/multi-agent-security](https://github.com/rexcoleman/multi-agent-security)

Framework is open source. Happy to answer questions about the simulation design or real-agent validation.
