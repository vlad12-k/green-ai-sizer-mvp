#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: bash scripts/run_co2e.sh [BUDGET_G_PER_1K]"
  echo "Example: bash scripts/run_co2e.sh 200"
}

BUDGET="${1:-200}"

if [[ "${BUDGET}" == "-h" || "${BUDGET}" == "--help" ]]; then
  usage
  exit 0
fi

if ! [[ "${BUDGET}" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: Budget must be a number (e.g., 200). Got: ${BUDGET}"
  usage
  exit 2
fi

python workbook/calc_co2e.py "${BUDGET}"
