# Evidence index

This index explains what each evidence file proves.

| Evidence file | What it proves |
|---|---|
| `data/scenario-baseline-improved.csv` | Versioned baseline vs improved scenario inputs used by CI budget calculations |
| `workbook/calc_co2e.py` | Deterministic carbon budget calculation logic used locally and in CI |
| `data/grid_intensity_uk_snapshot.csv` | Raw UK grid-intensity snapshot values used for reproducibility |
| `data/grid_intensity_uk_summary.json` | Min/avg/max grid intensity used in reporting and calculations |
| `scripts/probe_run_summary.json` | Observed endpoint behavior metrics (cache, routing, latency, Wh/request) |
| `scripts/probe_endpoint.py` | Reproducible method used to collect probe evidence |
| `.github/workflows/carbon-budget.yml` | Carbon budget enforcement gate in CI |
| `.github/workflows/refresh-grid-intensity.yml` | Scheduled/manual refresh, dashboard evidence sync, and direct commit to `main` when data changes |
| `docs/governance/controls.md` | Control objectives mapped to evidence and review cadence |
| `docs/governance/runbook.md` | Repeatable operational procedures for validation, refresh, and response |
| `docs/governance/risk-register.md` | Tracked risks, impacts, and mitigations |

See also: `docs/evidence/data-sources.md` for provenance and reproduction details.
