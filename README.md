[![Carbon Budget Gate](https://github.com/vlad12-k/green-ai-sizer-mvp/actions/workflows/carbon-budget.yml/badge.svg)](https://github.com/vlad12-k/green-ai-sizer-mvp/actions/workflows/carbon-budget.yml)

# Green AI Sizer MVP

## Problem
Climate-critical digital services operate under heatwave stress and grid volatility. AI usage can improve responsiveness, but unmanaged inference demand can silently increase baseline emissions and cost.

## Solution
Green AI Sizer MVP adds enforceable controls: a CI carbon budget gate, versioned scenario inputs, and auditable evidence for routing, caching, and grid-intensity assumptions so sustainability constraints stay operational rather than narrative.

## How it works
- CI runs `python workbook/calc_co2e.py 200` and fails when improved gCO₂e/1k exceeds budget.
- Scenario inputs are versioned in `data/scenario-baseline-improved.csv`.
- Grid data is refreshed into `data/grid_intensity_uk_snapshot.csv` and `data/grid_intensity_uk_summary.json`.
- Probe evidence is captured in `scripts/probe_run_summary.json`.
- GitHub Pages dashboard in `docs/` renders committed evidence files only.

## Quickstart
```bash
python workbook/calc_co2e.py 200
```

## Architecture
- Architecture docs: `docs/architecture/system-architecture.md`
- Dashboard entry point (Pages): `docs/index.html`

## Evidence & governance
- Evidence index: `docs/evidence/index.md`
- Data provenance: `docs/evidence/data-sources.md`
- Controls: `docs/governance/controls.md`
- Runbook: `docs/governance/runbook.md`
- Risk register: `docs/governance/risk-register.md`
- RACI: `docs/governance/raci.md`
- KPI definitions: `docs/governance/kpis.md`
- Migration mapping: `MIGRATION.md`

## Limitations
- Scenario method uses simplified energy-per-request estimates and UK average grid-intensity assumptions.
- Results are auditable and reproducible, but not full production carbon accounting.

## License
[MIT](LICENSE)


## Quality checks
Run all minimal production-grade checks locally:
```bash
make check
```
This runs tests for dashboard evidence loading/parsing, Carbon Budget Gate output fields, MIGRATION path resolution, plus a smoke validation script.
