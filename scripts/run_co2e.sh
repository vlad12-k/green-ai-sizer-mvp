#!/usr/bin/env bash
set -euo pipefail

BUDGET="${1:-200}"
python workbook/calc_co2e.py "${BUDGET}"
