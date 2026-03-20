# Substack Email Intro

> Paste BEFORE the full blog post content in Substack editor.

---

**Subject line:** I compromised one AI agent. It cascaded to 100% of the system.

I compromised one agent in a multi-agent system. Under default trust settings — the kind CrewAI, AutoGen, and LangGraph ship with — it cascaded to 100% of the system. Every time.

Zero-trust architecture cuts the poison rate by 40 percentage points, but an adaptive adversary recovers 54% of that advantage. I ran 6 experiments to quantify this.

The most surprising finding: 4 out of 6 of my hypotheses were wrong. Topology, agent type, and memory isolation don't matter. The only things that matter are trust model and adversary sophistication.

Read on for the full results, including the negative findings that narrow the solution space for anyone building secure multi-agent systems.
