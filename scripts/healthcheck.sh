#!/usr/bin/env bash
set -euo pipefail

echo "=== GitHub Actions Reusable Workflows Healthcheck ==="
python3 scripts/validate_workflows.py
echo "[OK] All workflow definitions verified."
exit 0
