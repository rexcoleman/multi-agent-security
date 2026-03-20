# LinkedIn Post — Multi-Agent Security

> Paste as native LinkedIn text. Add blog link as FIRST COMMENT.

---

I built a multi-agent security testing framework and ran 6 experiments to answer: what happens when ONE agent in your system gets compromised?

The results: under implicit trust (the default in CrewAI, AutoGen, and most frameworks), a single compromised agent cascades to 100% of the system. 97% of all decisions poisoned. Whether you have 2 agents or 10.

Zero-trust is the only defense that works — cutting poison rate by 40 percentage points. But here's the uncomfortable part: a defense-aware attacker recovers 54% of that advantage by crafting outputs that pass verification.

4 out of 6 of my predictions were wrong:

1. Topology doesn't matter. Hierarchical, flat, star — all reach 100% cascade.
2. Agent type doesn't matter. LLM, RL, rule-based — identical cascade dynamics.
3. Memory isolation barely helps. 1.2pp difference.
4. Credential theft is less dangerous than understanding the defense.

The only things that matter: trust model and adversary sophistication.

If you're building multi-agent systems, implement zero-trust verification at every delegation point. The default implicit trust provides zero containment.

Framework is open source. 6 experiments, 5 seeds, 16 tests.

What trust model does your multi-agent system use? I'd bet it's implicit.

#AISecurity #MultiAgent #ZeroTrust #MachineLearning #BuildInPublic

---

> First comment: "Full write-up with figures: [blog URL]"
> Second comment: "Code: github.com/rexcoleman/multi-agent-security"
