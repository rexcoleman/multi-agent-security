# Substack Email Intro

> Paste BEFORE the full blog post content in Substack editor.

---

If you're building with multi-agent AI systems — CrewAI, AutoGen, LangGraph — there's something you should know: the default trust model in every major framework provides zero containment against compromise.

I built a testing framework and ran 6 experiments to quantify the risk. A single compromised agent cascades to 100% of a system under implicit trust. Zero-trust architecture cuts the poison rate by 40 percentage points — but an adaptive adversary recovers 54% of that advantage.

The most surprising finding: 4 out of 6 of my hypotheses were wrong. Topology, agent type, and memory isolation don't matter. The only things that matter are trust model and adversary sophistication.

Read on for the full results, including the negative findings that narrow the solution space for anyone building secure multi-agent systems.
