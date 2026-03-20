#!/bin/bash
# FP-15: Full reproducible pipeline
set -e
echo "=== FP-15 Reproduce Pipeline ==="
echo "Date: $(date)"
echo "Git: $(git rev-parse --short HEAD 2>/dev/null || echo 'not a git repo')"

# Install deps
pip install -e ".[dev]" 2>&1 | tail -3

# Run tests
echo "--- Running tests ---"
python -m pytest tests/ -v

# Run all experiments
echo "--- Running experiments ---"
python scripts/run_experiments.py --config config/base.yaml

# Generate figures
echo "--- Generating figures ---"
python scripts/make_figures.py

echo "=== DONE: $(date) ==="

# --- Gate Validation (R50) ---
if [ -f "$HOME/ml-governance-templates/scripts/check_all_gates.sh" ]; then
    echo "--- Gate Validation (R50) ---"
    bash "$HOME/ml-governance-templates/scripts/check_all_gates.sh" .
else
    echo "WARN: govML not found — skipping gate validation (R50)"
fi
