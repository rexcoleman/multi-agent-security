# Distribution Draft: Reddit r/netsec
# Status: DRAFT — Rex must review and approve before posting
# Target: https://www.reddit.com/r/netsec/
# Blog URL: https://rexcoleman.dev/posts/agent-semantic-resistance/

---

## Title

I built a multi-agent cascade poisoning framework, then validated against real Claude agents — the simulation was wrong by 37 percentage points

## Body

I built a simulation-based testbed for multi-agent cascade poisoning — configurable trust models, topologies, attacker types. Ran 6 experiments, then validated against real Claude Haiku agents. The simulation predicted 97% poison rate under implicit trust. Real agents: 60%. And the simulation said topology doesn't matter — real agents proved it does (17pp spread).

**What I tested:**

Three trust models (implicit, capability-scoped, zero-trust). Three topologies (hierarchical, flat, star). Three attacker types (naive, defense-aware, credential-theft). Five seeds per experiment, 16 passing tests.

**Key results:**

| | Simulation | Real Agents | Gap |
|---|---|---|---|
| Implicit trust poison | 97.4% | 60.0% | 37pp |
| Zero-trust poison | 58.3% | 53.3% | 5pp |
| Topology matters? | No (all ~97%) | Yes (17pp spread) | Qualitatively wrong |

- **Zero-trust is the only defense that actually reduces cascade** — cuts poison by 40pp in simulation, confirmed as best on real agents
- **Capability-scoped trust barely helps** — 7pp in simulation, 0pp on real agents. More complexity for no gain.
- **Hierarchical topology is protective on real agents** — 56% poison vs 73% flat. The simulation missed this entirely because it doesn't model semantic resistance at different delegation depths.
- **Defense-aware attackers recover 54% of zero-trust's advantage** — if they know you're verifying, they craft outputs that pass. Static verification is insufficient.
- **What you say matters more than who you are** — credential theft (0.617 poison) is less effective than crafting convincing outputs (0.899). Identity-based trust is the wrong defense.
- **Memory isolation is nearly irrelevant** — only 1.2pp difference between shared and isolated memory. Direct delegation is the primary cascade channel.

**4 out of 6 pre-registered hypotheses were refuted.** The refutations are more valuable — they narrow the solution space. The only things that matter for cascade defense: trust model and adversary sophistication. Topology, agent type, and memory mode don't move the needle in simulation (though topology does matter on real agents).

**Methodology:** Simulation with configurable parameters, validated against real Claude Haiku agents (3 seeds, 5 tasks per seed). All hypotheses pre-registered in HYPOTHESIS_REGISTRY.md before experiments. E0 sanity validation (positive control, negative control, dose-response) before any experiments.

**Limitations:** Simulation overestimates severity by 37pp vs real agents. Fixed cascade probability (0.15, tuned for differentiation). 5 agents max in most experiments. Single compromised agent (orchestrator). Static payloads.

Repo is open source: https://github.com/rexcoleman/multi-agent-security

Full write-up with figures: https://rexcoleman.dev/posts/agent-semantic-resistance/

Happy to answer methodology questions. The simulation-to-real gap is the main contribution — it shows what simulation-only agent security research gets wrong.
