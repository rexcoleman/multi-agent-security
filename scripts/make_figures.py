#!/usr/bin/env python3
"""Generate publication-quality figures for FP-15.

Reads experiment results from outputs/experiments/ and generates PNGs.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

INPUT_DIR = Path("outputs/experiments")
OUTPUT_DIR = Path("outputs/figures")
BLOG_DIR = Path("blog/images")

DPI = 300
FIGSIZE = (10, 6)

# Style
sns.set_theme(style="whitegrid", font_scale=1.2)
COLORS = sns.color_palette("husl", 6)


def load_results(exp_id: str) -> dict:
    path = INPUT_DIR / f"{exp_id.lower()}_results.json"
    with open(path) as f:
        return json.load(f)


def fig_e1_cascade_vs_count():
    """Bar chart: cascade rate vs number of agents."""
    data = load_results("E1")
    summary = data["summary"]

    counts = sorted(summary.keys(), key=int)
    means = [summary[c]["cascade_rate_mean"] for c in counts]
    stds = [summary[c]["cascade_rate_std"] for c in counts]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    bars = ax.bar(range(len(counts)), means, yerr=stds, capsize=5,
                  color=COLORS[0], edgecolor="black", alpha=0.85)
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts)
    ax.set_xlabel("Number of Agents")
    ax.set_ylabel("Cascade Rate (fraction compromised)")
    ax.set_title("E1: Single-Agent Compromise Cascades with Agent Count")
    ax.set_ylim(0, 1.05)

    # Add value labels
    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f"{mean:.2f}", ha="center", va="bottom", fontsize=10)

    fig.tight_layout()
    for d in [OUTPUT_DIR, BLOG_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        fig.savefig(d / "e1_cascade_vs_count.png", dpi=DPI)
    plt.close()
    print("  Saved: e1_cascade_vs_count.png")


def fig_e2_trust_model():
    """Grouped bar chart: cascade + poison rate by trust model."""
    data = load_results("E2")
    summary = data["summary"]

    models = list(summary.keys())
    cascade_means = [summary[m]["cascade_rate_mean"] for m in models]
    cascade_stds = [summary[m]["cascade_rate_std"] for m in models]
    poison_means = [summary[m]["poison_rate_mean"] for m in models]
    poison_stds = [summary[m]["poison_rate_std"] for m in models]

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=FIGSIZE)
    bars1 = ax.bar(x - width/2, cascade_means, width, yerr=cascade_stds,
                   label="Cascade Rate", color=COLORS[1], capsize=5, alpha=0.85)
    bars2 = ax.bar(x + width/2, poison_means, width, yerr=poison_stds,
                   label="Poison Rate", color=COLORS[2], capsize=5, alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("_", " ").title() for m in models])
    ax.set_ylabel("Rate")
    ax.set_title("E2: Trust Model Impact on Cascade Propagation (5 agents)")
    ax.legend()
    ax.set_ylim(0, 1.05)

    fig.tight_layout()
    for d in [OUTPUT_DIR, BLOG_DIR]:
        fig.savefig(d / "e2_trust_model.png", dpi=DPI)
    plt.close()
    print("  Saved: e2_trust_model.png")


def fig_e3_topology():
    """Bar chart: cascade rate by topology."""
    data = load_results("E3")
    summary = data["summary"]

    topos = list(summary.keys())
    means = [summary[t]["cascade_rate_mean"] for t in topos]
    stds = [summary[t]["cascade_rate_std"] for t in topos]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    bars = ax.bar(range(len(topos)), means, yerr=stds, capsize=5,
                  color=[COLORS[3], COLORS[4], COLORS[5]], edgecolor="black", alpha=0.85)
    ax.set_xticks(range(len(topos)))
    ax.set_xticklabels([t.title() for t in topos])
    ax.set_xlabel("Network Topology")
    ax.set_ylabel("Cascade Rate")
    ax.set_title("E3: Topology Impact on Cascade Propagation (5 agents, implicit trust)")
    ax.set_ylim(0, 1.05)

    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f"{mean:.2f}", ha="center", va="bottom", fontsize=10)

    fig.tight_layout()
    for d in [OUTPUT_DIR, BLOG_DIR]:
        fig.savefig(d / "e3_topology.png", dpi=DPI)
    plt.close()
    print("  Saved: e3_topology.png")


def fig_e4_adaptive():
    """Bar chart: adaptive adversary effectiveness vs zero-trust."""
    data = load_results("E4")
    summary = data["summary"]

    attackers = list(summary.keys())
    means = [summary[a]["cascade_rate_mean"] for a in attackers]
    stds = [summary[a]["cascade_rate_std"] for a in attackers]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    bars = ax.bar(range(len(attackers)), means, yerr=stds, capsize=5,
                  color=[COLORS[0], COLORS[1], COLORS[2]], edgecolor="black", alpha=0.85)
    ax.set_xticks(range(len(attackers)))
    ax.set_xticklabels([a.replace("_", " ").title() for a in attackers])
    ax.set_xlabel("Attacker Type")
    ax.set_ylabel("Cascade Rate")
    ax.set_title("E4: Adaptive Adversary vs Zero-Trust Defense (5 agents)")
    ax.set_ylim(0, 1.05)

    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f"{mean:.2f}", ha="center", va="bottom", fontsize=10)

    fig.tight_layout()
    for d in [OUTPUT_DIR, BLOG_DIR]:
        fig.savefig(d / "e4_adaptive_adversary.png", dpi=DPI)
    plt.close()
    print("  Saved: e4_adaptive_adversary.png")


def fig_e5_mixed():
    """Bar chart: cascade rate by agent composition."""
    data = load_results("E5")
    summary = data["summary"]

    comps = list(summary.keys())
    means = [summary[c]["cascade_rate_mean"] for c in comps]
    stds = [summary[c]["cascade_rate_std"] for c in comps]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    bars = ax.bar(range(len(comps)), means, yerr=stds, capsize=5,
                  color=COLORS[:len(comps)], edgecolor="black", alpha=0.85)
    ax.set_xticks(range(len(comps)))
    ax.set_xticklabels([c.replace("_", "\n") for c in comps], fontsize=9)
    ax.set_xlabel("Agent Composition")
    ax.set_ylabel("Cascade Rate")
    ax.set_title("E5: Agent Type Composition Impact on Cascade (5 agents, implicit trust)")
    ax.set_ylim(0, 1.05)

    fig.tight_layout()
    for d in [OUTPUT_DIR, BLOG_DIR]:
        fig.savefig(d / "e5_mixed_agents.png", dpi=DPI)
    plt.close()
    print("  Saved: e5_mixed_agents.png")


def fig_e6_memory():
    """Bar chart: memory mode impact on cascade."""
    data = load_results("E6")
    summary = data["summary"]

    modes = list(summary.keys())
    means = [summary[m]["cascade_rate_mean"] for m in modes]
    stds = [summary[m]["cascade_rate_std"] for m in modes]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    bars = ax.bar(range(len(modes)), means, yerr=stds, capsize=5,
                  color=[COLORS[3], COLORS[4], COLORS[5]], edgecolor="black", alpha=0.85)
    ax.set_xticks(range(len(modes)))
    ax.set_xticklabels([m.title() for m in modes])
    ax.set_xlabel("Memory Mode")
    ax.set_ylabel("Cascade Rate")
    ax.set_title("E6: Shared Memory Impact on Cascade Propagation (5 agents)")
    ax.set_ylim(0, 1.05)

    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f"{mean:.2f}", ha="center", va="bottom", fontsize=10)

    fig.tight_layout()
    for d in [OUTPUT_DIR, BLOG_DIR]:
        fig.savefig(d / "e6_memory_ablation.png", dpi=DPI)
    plt.close()
    print("  Saved: e6_memory_ablation.png")


def fig_cascade_over_time():
    """Line plot: cascade rate over time for E2 trust models."""
    data = load_results("E2")
    raw = data["raw"]["results"]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    for i, (model, seed_results) in enumerate(raw.items()):
        # Average cascade_over_time across seeds
        all_curves = [r["cascade_over_time"] for r in seed_results]
        min_len = min(len(c) for c in all_curves)
        trimmed = [c[:min_len] for c in all_curves]
        mean_curve = np.mean(trimmed, axis=0)
        std_curve = np.std(trimmed, axis=0)
        steps = range(len(mean_curve))
        ax.plot(steps, mean_curve, label=model.replace("_", " ").title(),
                color=COLORS[i], linewidth=2)
        ax.fill_between(steps, mean_curve - std_curve, mean_curve + std_curve,
                        alpha=0.2, color=COLORS[i])

    ax.set_xlabel("Time Step")
    ax.set_ylabel("Cascade Rate (fraction compromised)")
    ax.set_title("Cascade Propagation Over Time by Trust Model (5 agents)")
    ax.legend()
    ax.set_ylim(0, 1.05)

    fig.tight_layout()
    for d in [OUTPUT_DIR, BLOG_DIR]:
        fig.savefig(d / "cascade_over_time.png", dpi=DPI)
    plt.close()
    print("  Saved: cascade_over_time.png")


def main():
    print("Generating FP-15 figures...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    fig_e1_cascade_vs_count()
    fig_e2_trust_model()
    fig_e3_topology()
    fig_e4_adaptive()
    fig_e5_mixed()
    fig_e6_memory()
    fig_cascade_over_time()

    print(f"\nAll figures saved to {OUTPUT_DIR} and {BLOG_DIR}")


if __name__ == "__main__":
    main()
