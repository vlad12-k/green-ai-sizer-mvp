# System Boundary — Assumptions and system boundary

## System boundary (what is included)

This emissions method covers operational emissions for:

- Inference orchestration (routing and fallback logic)
- Caching (response / semantic cache)
- Logging and metrics needed to compute KPIs
- Network overhead (simplified; treated as negligible at MVP scope)

## Exclusions (what is NOT included)

- End-user device energy use
- Embodied emissions of hardware (manufacture and disposal)
- Full data centre PUE modelling (deferred to a future iteration)
- Azure infrastructure overhead beyond the Function App

## Core assumptions (current values — sourced from evidence files)

| Parameter | Value | Source |
|---|---|---|
| Requests per day (baseline + improved) | 1,000 | `data/scenario-baseline-improved.csv` |
| Cache hit rate (baseline) | 0 % | `data/scenario-baseline-improved.csv` |
| Cache hit rate (improved) | 31 % | `scripts/probe_run_summary.json` → CSV |
| Small route rate (baseline) | 0 % | `data/scenario-baseline-improved.csv` |
| Small route rate (improved) | 60 % | `scripts/probe_run_summary.json` → CSV |
| Energy per small request (Wh) | 0.2 | `data/scenario-baseline-improved.csv` |
| Energy per large request (Wh) | 2.0 | `data/scenario-baseline-improved.csv` |
| Grid carbon intensity (gCO₂/kWh) | 79.85 (avg, UK national grid) | `data/grid_intensity_uk_summary.json` |

## Sensitivity

The grid intensity input can be varied between min (40.0 gCO₂/kWh) and max (135.0 gCO₂/kWh) — see `data/grid_intensity_uk_summary.json` — to assess best-case and worst-case CO₂e outcomes. The CI gate uses the average value for the pass/fail decision.

## Limitations

- Grid intensity represents the UK national grid mix at snapshot time; it is not marginal emissions.
- Forecast intensity is used for consistency with the NESO API output.
- Wh-per-request values are estimates based on small/large model routing ratios; they are not measured from hardware telemetry.
- PUE is not applied; results are conservative (understated) relative to real-world data centre overhead.
