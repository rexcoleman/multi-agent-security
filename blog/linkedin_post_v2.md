# Distribution Draft: LinkedIn
# Status: DRAFT — Rex must review and approve before posting
# Instructions: Paste as native LinkedIn text. Blog link goes in FIRST COMMENT.

---

I tested cascade poisoning on real LLM agents. My simulation predicted 97% poison rate. Real Claude Haiku agents: 60%.

The simulation was wrong by 37 percentage points. And the biggest surprise: topology matters — something the simulation said was irrelevant.

Three things I got wrong:

→ Capability-scoped trust barely helps. 7pp in simulation, 0pp on real agents.
→ Topology is irrelevant. Wrong. Hierarchical (56% poison) beats flat (73%) by 17pp.
→ Memory isolation is a major defense. Wrong. Only 1.2pp difference.

One thing I got right:

→ Zero-trust is the only defense that works. Cuts poison by 40pp in simulation, confirmed as best on real agents too.

The uncomfortable part: a defense-aware attacker recovers 54% of zero-trust's advantage by crafting outputs that pass verification.

If you're building with CrewAI, AutoGen, or any multi-agent framework: implement zero-trust verification at every delegation point. The default implicit trust provides zero containment.

4 out of 6 hypotheses refuted. The refutations narrowed the solution space more than the confirmations.

Link in comments.

#AISecurity #MultiAgent #ZeroTrust #LLMSecurity

---

# First comment: "Full write-up with figures and methodology: https://rexcoleman.dev/posts/agent-semantic-resistance/"
# Second comment: "Code: https://github.com/rexcoleman/multi-agent-security"
