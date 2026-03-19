#!/usr/bin/env python3
"""Parameter sensitivity sweep — validates findings are robust across base_prob values.

Addresses G-5: "You tuned the parameters to get the results you wanted."
Sweeps base cascade probability and shows E2 (trust model) and E4 (adaptive)
findings hold qualitatively across the parameter space.

Usage:
    python scripts/run_sensitivity.py
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.attacker import apply_attack
from src.network import AgentNetwork

OUTPUT_DIR = Path("outputs/experiments")
SEEDS = [42, 123, 456, 789, 1024]
BASE_PROBS = [0.05, 0.10, 0.15, 0.20, 0.30, 0.50]


def run_with_prob(base_prob, trust_model, seed, attacker_type="naive",
                  n_agents=5, topology="hierarchical", time_steps=20):
    """Run simulation with a specific base cascade probability."""
    net = AgentNetwork(
        n_agents=n_agents, topology=topology,
        trust_model_name=trust_model, seed=seed,
    )
    # Monkey-patch the cascade probability
    original_method = net._cascade_probability
    def patched_cascade_prob(agent, task):
        prob = original_method(agent, task)
        # Scale by ratio of new base_prob to default (0.15)
        return min(prob * (base_prob / 0.15), 1.0)
    net._cascade_probability = patched_cascade_prob

    apply_attack(net, attacker_type, target_id=0)
    metrics = net.run_simulation(time_steps=time_steps)
    return metrics.to_dict()


def run_e2_sensitivity():
    """E2 trust model comparison across base_prob values."""
    print("=" * 60)
    print("SENSITIVITY: E2 Trust Model across base_prob")
    print("=" * 60)

    results = {}
    for bp in BASE_PROBS:
        results[str(bp)] = {}
        for trust in ["implicit", "capability_scoped", "zero_trust"]:
            seed_results = []
            for seed in SEEDS:
                m = run_with_prob(bp, trust, seed)
                seed_results.append(m)

            cascade_rates = [r["cascade_rate"] for r in seed_results]
            poison_rates = [r["poison_rate"] for r in seed_results]
            results[str(bp)][trust] = {
                "cascade_mean": float(np.mean(cascade_rates)),
                "cascade_std": float(np.std(cascade_rates)),
                "poison_mean": float(np.mean(poison_rates)),
                "poison_std": float(np.std(poison_rates)),
            }

        # Print row
        imp = results[str(bp)]["implicit"]
        zt = results[str(bp)]["zero_trust"]
        reduction = imp["poison_mean"] - zt["poison_mean"]
        pct = (reduction / imp["poison_mean"] * 100) if imp["poison_mean"] > 0 else 0
        print(f"  base_prob={bp:.2f}: implicit={imp['poison_mean']:.3f}, "
              f"zero_trust={zt['poison_mean']:.3f}, reduction={reduction:.3f} ({pct:.0f}%)")

    return results


def run_e4_sensitivity():
    """E4 adaptive adversary across base_prob values."""
    print("\n" + "=" * 60)
    print("SENSITIVITY: E4 Adaptive Adversary across base_prob")
    print("=" * 60)

    results = {}
    for bp in BASE_PROBS:
        results[str(bp)] = {}
        for attacker in ["naive", "defense_aware", "credential_theft"]:
            seed_results = []
            for seed in SEEDS:
                m = run_with_prob(bp, "zero_trust", seed, attacker_type=attacker)
                seed_results.append(m)

            poison_rates = [r["poison_rate"] for r in seed_results]
            results[str(bp)][attacker] = {
                "poison_mean": float(np.mean(poison_rates)),
                "poison_std": float(np.std(poison_rates)),
            }

        naive = results[str(bp)]["naive"]["poison_mean"]
        aware = results[str(bp)]["defense_aware"]["poison_mean"]
        recovery = (aware - naive) / max(1.0 - naive, 0.01) * 100
        print(f"  base_prob={bp:.2f}: naive={naive:.3f}, "
              f"defense_aware={aware:.3f}, recovery={recovery:.0f}%")

    return results


def run_inflection_analysis():
    """Find the time step where zero-trust diverges from implicit."""
    print("\n" + "=" * 60)
    print("MECHANISM: E2 Inflection Point Analysis")
    print("=" * 60)

    results = {}
    for trust in ["implicit", "capability_scoped", "zero_trust"]:
        all_curves = []
        for seed in SEEDS:
            net = AgentNetwork(n_agents=5, topology="hierarchical",
                              trust_model_name=trust, seed=seed)
            apply_attack(net, "naive", target_id=0)
            metrics = net.run_simulation(time_steps=20)
            all_curves.append(metrics.to_dict()["cascade_over_time"])

        min_len = min(len(c) for c in all_curves)
        trimmed = [c[:min_len] for c in all_curves]
        mean_curve = np.mean(trimmed, axis=0)
        results[trust] = [float(v) for v in mean_curve]

        # Find inflection: first step where cascade > 0.5
        inflection = next((i for i, v in enumerate(mean_curve) if v > 0.5), -1)
        print(f"  {trust}: inflection at step {inflection}, "
              f"final cascade={mean_curve[-1]:.3f}")

    return results


def run_verification_threshold_sweep():
    """Sweep zero-trust verification_prob to find minimum effective threshold."""
    print("\n" + "=" * 60)
    print("MECHANISM: Verification Probability Threshold Sweep")
    print("=" * 60)

    thresholds = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    results = {}

    for vp in thresholds:
        seed_results = []
        for seed in SEEDS:
            net = AgentNetwork(n_agents=5, topology="hierarchical",
                              trust_model_name="zero_trust", seed=seed)
            net.trust_model.verification_prob = vp
            apply_attack(net, "naive", target_id=0)
            metrics = net.run_simulation(time_steps=20)
            seed_results.append(metrics.to_dict())

        cascade_rates = [r["cascade_rate"] for r in seed_results]
        poison_rates = [r["poison_rate"] for r in seed_results]
        results[str(vp)] = {
            "cascade_mean": float(np.mean(cascade_rates)),
            "poison_mean": float(np.mean(poison_rates)),
        }
        print(f"  verification_prob={vp:.1f}: cascade={np.mean(cascade_rates):.3f}, "
              f"poison={np.mean(poison_rates):.3f}")

    return results


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("FP-15 Parameter Sensitivity + Mechanism Analysis")
    print(f"Seeds: {SEEDS}")
    print(f"Base probs: {BASE_PROBS}\n")

    e2_sens = run_e2_sensitivity()
    e4_sens = run_e4_sensitivity()
    inflection = run_inflection_analysis()
    threshold = run_verification_threshold_sweep()

    # Save all results
    all_results = {
        "date": datetime.now().isoformat(),
        "seeds": SEEDS,
        "base_probs": BASE_PROBS,
        "e2_sensitivity": e2_sens,
        "e4_sensitivity": e4_sens,
        "inflection_analysis": inflection,
        "verification_threshold": threshold,
    }

    out_file = OUTPUT_DIR / "sensitivity_analysis.json"
    with open(out_file, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved: {out_file}")

    # Summary: is the zero-trust finding robust?
    print("\n" + "=" * 60)
    print("ROBUSTNESS CHECK: Is zero-trust advantage consistent?")
    print("=" * 60)
    for bp in BASE_PROBS:
        imp = e2_sens[str(bp)]["implicit"]["poison_mean"]
        zt = e2_sens[str(bp)]["zero_trust"]["poison_mean"]
        if imp > 0:
            pct = (imp - zt) / imp * 100
            print(f"  base_prob={bp:.2f}: zero-trust reduces poison by {pct:.0f}% relative")
        else:
            print(f"  base_prob={bp:.2f}: no cascade (base_prob too low)")


if __name__ == "__main__":
    main()
