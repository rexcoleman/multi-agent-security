# DECISION LOG — FP-15 Multi-Agent Security

## ADR-0001: Simulation-based testbed instead of real LLM agents
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** Real LLM agent experiments require API costs ($50-100+ per full experiment suite) and introduce non-determinism from model updates. Need reproducible, seed-controlled results.
- **Decision:** Build simulation-based testbed with probabilistic agent models. Validates framework design and cascade dynamics. Real LLM validation deferred to Phase 2.
- **Consequences:** Results are simulation-based, not empirical LLM behavior. Acknowledged in Limitations. The simulation establishes the FRAMEWORK; real-agent validation is the next step.

## ADR-0002: Base cascade probability tuned to 0.15
- **Date:** 2026-03-19 | **Phase:** 1
- **Context:** Initial cascade probability (0.40) caused 100% cascade saturation across all conditions within 5 time steps, eliminating differentiation between trust models.
- **Decision:** Tuned base_prob to 0.15 for differentiation. Zero-trust modifier (0.2x) produces meaningful cascade reduction.
- **Consequences:** Absolute rates are parameter-dependent. Paper reports relative comparisons between conditions, not absolute rates. Acknowledged in Limitations.

## ADR-0003: CrewAI evaluation deferred — custom framework used
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** EXPERIMENTAL_DESIGN.md specified CrewAI + custom harness. CrewAI requires API keys and adds external dependency. For Phase 1, custom simulation provides more control.
- **Decision:** Phase 1 uses custom simulation framework. CrewAI integration planned for Phase 2 (real LLM validation).
- **Consequences:** Results demonstrate framework capability, not CrewAI-specific behavior. Reviewer kill shot #2 (toy frameworks) partially addressed by custom harness, fully addressed when CrewAI integration is added.
