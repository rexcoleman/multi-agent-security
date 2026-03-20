# For: OpenClaw Discord

if you run multiple OpenClaw agents (work agent, personal agent, research agent), the default implicit trust between them means a compromised skill cascades to all agents. I built a multi-agent cascade simulation and validated against real Claude agents.

```
                    simulation   real agents   gap
implicit trust      97.4%        60.0%         37pp
zero-trust          58.3%        53.3%          5pp

topology matters:
hierarchical: 56% (most protected)
flat:         73% (worst)
star:         71%
```

flat topology is the worst — every agent trusts every other agent equally. if your OpenClaw setup has agents sharing memory or passing context without verification, one poisoned skill output propagates to 73% of connected agents.

zero-trust is the only trust model that actually reduces cascade. but even then, a defense-aware attacker recovers 54% of the gap. hierarchical topology (one coordinator agent that delegates to specialized agents) is the most protected architecture.

for OpenClaw: if your agents share memory pools or delegate tasks between each other, the trust model between them matters more than any individual agent's SOUL.md rules. a compromised personal agent with access to your work agent's memory is the real threat — not a direct attack on a hardened work agent.

practical question: does OpenClaw have a way to set per-agent trust boundaries on shared memory? or is it implicit trust by default between agents in the same config?
