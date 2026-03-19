# CONTENT PLAN — FP-15 Multi-Agent Security Testing Framework

> **Project:** FP-15 (Multi-Agent Security)
> **Created:** 2026-03-19
> **Status:** Blog drafted, conference abstract drafted, 0 published

---

## Content Assets

| ID | Type | Title | Status | Target | Path |
|----|------|-------|--------|--------|------|
| C-01 | Blog post | Your Multi-Agent System Has a 97% Poison Rate | DRAFTED | rexcoleman.dev | `blog/draft.md` |
| C-02 | LinkedIn post | Multi-agent cascade findings | DRAFTED | LinkedIn | `blog/linkedin_post.md` |
| C-03 | Substack intro | Multi-agent security email hook | DRAFTED | Substack | `blog/substack_intro.md` |
| C-04 | Conference abstract | AISec Workshop (ACM CCS 2026) | DRAFTED | AISec | `blog/conference_abstract.md` |
| C-05 | TIL | "Implicit trust = zero containment at any scale" | PLANNED | dev.to | — |
| C-06 | TIL | "Zero-trust for AI agents, not just networks" | PLANNED | dev.to | — |
| C-07 | TIL | "Your zero-trust agent architecture has a 54% hole" | PLANNED | dev.to | — |
| C-08 | TIL | "Reorganizing your agent network won't save you" | PLANNED | dev.to | — |
| C-09 | TIL | "I was wrong about 4/6 predictions — and that's the finding" | PLANNED | dev.to | — |
| C-10 | TIL | "Identity matters less than output quality in agent trust" | PLANNED | dev.to | — |
| C-11 | Thread | Twitter/X: 6 experiments, 4 wrong predictions, 1 defense | PLANNED | Twitter/X | — |
| C-12 | Talk slides | Conference talk deck (20 min) | PLANNED | AISec | — |
| C-13 | GitHub README | Project showcase for profile | PLANNED | GitHub | — |

---

## Key Messages

1. **Implicit trust = zero containment.** 100% cascade at any system size under the default trust model.
2. **Zero-trust is the only effective defense.** 40pp poison rate reduction. Nothing else works.
3. **Adaptive adversaries recover 54%.** Static verification is insufficient. Need defense-in-depth.
4. **Negative results narrow the solution space.** Topology, agent type, memory mode don't matter.
5. **The agent economy needs security testing frameworks.** No open-source option existed before this.

---

## Figures Available

| Figure | Path | Best Use |
|--------|------|----------|
| Cascade vs agent count | `blog/images/e1_cascade_vs_count.png` | C-01, C-05 |
| Trust model comparison | `blog/images/e2_trust_model.png` | C-01, C-06 |
| Topology comparison | `blog/images/e3_topology.png` | C-01, C-08 |
| Adaptive adversary | `blog/images/e4_adaptive_adversary.png` | C-01, C-07 |
| Mixed agents | `blog/images/e5_mixed_agents.png` | C-01, C-09 |
| Memory ablation | `blog/images/e6_memory_ablation.png` | C-01 |
| Cascade over time | `blog/images/cascade_over_time.png` | C-01, C-06 |
