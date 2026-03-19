#!/usr/bin/env python3
"""Run all FP-15 experiments (E1-E6) across 5 seeds.

Usage:
    python scripts/run_experiments.py --config config/base.yaml
    python scripts/run_experiments.py --config config/base.yaml --experiments E1,E2
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.attacker import apply_attack
from src.network import AgentNetwork

OUTPUT_DIR = Path("outputs/experiments")


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def run_single(
    n_agents, topology, trust_model, seed, time_steps=20,
    agent_types=None, memory_mode="shared", attacker_type="naive",
):
    """Run one simulation and return metrics dict."""
    net = AgentNetwork(
        n_agents=n_agents,
        topology=topology,
        trust_model_name=trust_model,
        agent_types=agent_types,
        memory_mode=memory_mode,
        seed=seed,
    )
    apply_attack(net, attacker_type, target_id=0)
    metrics = net.run_simulation(time_steps=time_steps)
    return metrics.to_dict()


def run_e1(config: dict, seeds: list) -> dict:
    """E1: Cascade propagation rate vs number of agents."""
    exp = config["experiments"]["E1_cascade_vs_count"]
    print(f"\n{'='*60}\nE1: Cascade vs Agent Count\n{'='*60}")
    results = {}
    for n in exp["agent_counts"]:
        seed_results = []
        for seed in seeds:
            m = run_single(n, exp["topology"], exp["trust_model"], seed, exp["time_steps"])
            seed_results.append(m)
            print(f"  n={n}, seed={seed}: cascade={m['cascade_rate']:.3f}, poison={m['poison_rate']:.3f}")
        results[str(n)] = seed_results
    return {"experiment": "E1_cascade_vs_count", "results": results}


def run_e2(config: dict, seeds: list) -> dict:
    """E2: Trust model comparison."""
    exp = config["experiments"]["E2_trust_model"]
    print(f"\n{'='*60}\nE2: Trust Model Comparison\n{'='*60}")
    results = {}
    for trust in exp["trust_models"]:
        seed_results = []
        for seed in seeds:
            m = run_single(exp["agent_count"], exp["topology"], trust, seed, exp["time_steps"])
            seed_results.append(m)
            print(f"  trust={trust}, seed={seed}: cascade={m['cascade_rate']:.3f}, poison={m['poison_rate']:.3f}")
        results[trust] = seed_results
    return {"experiment": "E2_trust_model", "results": results}


def run_e3(config: dict, seeds: list) -> dict:
    """E3: Topology comparison."""
    exp = config["experiments"]["E3_topology"]
    print(f"\n{'='*60}\nE3: Topology Comparison\n{'='*60}")
    results = {}
    for topo in exp["topologies"]:
        seed_results = []
        for seed in seeds:
            m = run_single(exp["agent_count"], topo, exp["trust_model"], seed, exp["time_steps"])
            seed_results.append(m)
            print(f"  topology={topo}, seed={seed}: cascade={m['cascade_rate']:.3f}, poison={m['poison_rate']:.3f}")
        results[topo] = seed_results
    return {"experiment": "E3_topology", "results": results}


def run_e4(config: dict, seeds: list) -> dict:
    """E4: Adaptive adversary vs zero-trust."""
    exp = config["experiments"]["E4_adaptive_adversary"]
    print(f"\n{'='*60}\nE4: Adaptive Adversary\n{'='*60}")
    results = {}
    for attacker in exp["attacker_types"]:
        seed_results = []
        for seed in seeds:
            m = run_single(
                exp["agent_count"], exp["topology"], exp["trust_model"],
                seed, exp["time_steps"], attacker_type=attacker,
            )
            seed_results.append(m)
            print(f"  attacker={attacker}, seed={seed}: cascade={m['cascade_rate']:.3f}, poison={m['poison_rate']:.3f}")
        results[attacker] = seed_results
    return {"experiment": "E4_adaptive_adversary", "results": results}


def run_e5(config: dict, seeds: list) -> dict:
    """E5: Mixed agent type composition."""
    exp = config["experiments"]["E5_mixed_agents"]
    print(f"\n{'='*60}\nE5: Mixed Agent Types\n{'='*60}")
    results = {}
    for comp_name, comp in exp["compositions"].items():
        seed_results = []
        for seed in seeds:
            m = run_single(
                exp["agent_count"], exp["topology"], exp["trust_model"],
                seed, exp["time_steps"], agent_types=comp,
            )
            seed_results.append(m)
            print(f"  comp={comp_name}, seed={seed}: cascade={m['cascade_rate']:.3f}, poison={m['poison_rate']:.3f}")
        results[comp_name] = seed_results
    return {"experiment": "E5_mixed_agents", "results": results}


def run_e6(config: dict, seeds: list) -> dict:
    """E6: Shared memory ablation."""
    exp = config["experiments"]["E6_memory_ablation"]
    print(f"\n{'='*60}\nE6: Memory Ablation\n{'='*60}")
    results = {}
    for mode in exp["memory_modes"]:
        seed_results = []
        for seed in seeds:
            m = run_single(
                exp["agent_count"], exp["topology"], exp["trust_model"],
                seed, exp["time_steps"], memory_mode=mode,
            )
            seed_results.append(m)
            print(f"  memory={mode}, seed={seed}: cascade={m['cascade_rate']:.3f}, poison={m['poison_rate']:.3f}")
        results[mode] = seed_results
    return {"experiment": "E6_memory_ablation", "results": results}


def aggregate_results(experiment_results: dict) -> dict:
    """Compute mean +/- std across seeds for each condition."""
    summary = {}
    for condition, seed_results in experiment_results["results"].items():
        cascade_rates = [r["cascade_rate"] for r in seed_results]
        poison_rates = [r["poison_rate"] for r in seed_results]
        summary[condition] = {
            "cascade_rate_mean": float(np.mean(cascade_rates)),
            "cascade_rate_std": float(np.std(cascade_rates)),
            "poison_rate_mean": float(np.mean(poison_rates)),
            "poison_rate_std": float(np.std(poison_rates)),
            "n_seeds": len(seed_results),
        }
    return summary


def main():
    parser = argparse.ArgumentParser(description="Run FP-15 experiments")
    parser.add_argument("--config", default="config/base.yaml")
    parser.add_argument("--experiments", default="E1,E2,E3,E4,E5,E6",
                        help="Comma-separated experiment IDs")
    args = parser.parse_args()

    config = load_config(args.config)
    seeds = config["seeds"]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    experiments = {
        "E1": run_e1, "E2": run_e2, "E3": run_e3,
        "E4": run_e4, "E5": run_e5, "E6": run_e6,
    }

    requested = [e.strip() for e in args.experiments.split(",")]
    all_results = {}
    all_summaries = {}

    print(f"FP-15 Multi-Agent Security Experiments")
    print(f"Seeds: {seeds}")
    print(f"Experiments: {requested}")

    for exp_id in requested:
        if exp_id not in experiments:
            print(f"WARNING: Unknown experiment {exp_id}, skipping")
            continue

        result = experiments[exp_id](config, seeds)
        summary = aggregate_results(result)
        all_results[exp_id] = result
        all_summaries[exp_id] = summary

        # Save per-experiment
        out_file = OUTPUT_DIR / f"{exp_id.lower()}_results.json"
        with open(out_file, "w") as f:
            json.dump({"raw": result, "summary": summary, "seeds": seeds,
                        "date": datetime.now().isoformat()}, f, indent=2)
        print(f"  Saved: {out_file}")

    # Save combined summary
    combined_file = OUTPUT_DIR / "all_experiments_summary.json"
    with open(combined_file, "w") as f:
        json.dump({
            "date": datetime.now().isoformat(),
            "seeds": seeds,
            "summaries": all_summaries,
        }, f, indent=2)
    print(f"\nSaved combined: {combined_file}")

    # Print summary table
    print(f"\n{'='*80}")
    print("EXPERIMENT SUMMARY (mean +/- std across {len(seeds)} seeds)")
    print(f"{'='*80}")
    for exp_id, summary in all_summaries.items():
        print(f"\n--- {exp_id} ---")
        print(f"  {'Condition':<25} {'Cascade Rate':>18} {'Poison Rate':>18}")
        print(f"  {'-'*25} {'-'*18} {'-'*18}")
        for condition, stats in summary.items():
            cr = f"{stats['cascade_rate_mean']:.3f}+/-{stats['cascade_rate_std']:.3f}"
            pr = f"{stats['poison_rate_mean']:.3f}+/-{stats['poison_rate_std']:.3f}"
            print(f"  {condition:<25} {cr:>18} {pr:>18}")


if __name__ == "__main__":
    main()
