# Dashboard data contracts (Green AI Sizer Console)

The dashboard is static and reads only committed files under `docs/evidence/`.

## Required files
- `docs/evidence/grid_intensity_uk_summary.json`
- `docs/evidence/probe_run_summary.json`
- `docs/evidence/scenario-baseline-improved.csv`

## Contract: `grid_intensity_uk_summary.json`
Required keys:
- `generated_utc` (ISO timestamp string)
- `min_g_per_kwh` (number)
- `avg_g_per_kwh` (number)
- `max_g_per_kwh` (number)

Used for:
- Last updated label
- Grid intensity KPI cards (min/avg/max)

## Contract: `probe_run_summary.json`
Required keys:
- `cache_hit_rate_observed` (number in [0,1])
- `small_route_rate_observed` (number in [0,1])
- `p95_latency_ms` (number; optional for partial-load state)

Used for:
- Cache hit rate, small-route rate, p95 latency cards

## Contract: `scenario-baseline-improved.csv`
Required header columns:
- `scenario`
- `requests_per_day`
- `cache_hit_rate`
- `small_route_rate`
- `wh_small`
- `wh_large`
- `grid_intensity_g_per_kwh`

Required rows:
- `scenario=baseline`
- `scenario=improved`

Used for:
- Baseline and improved gCO₂e/1k cards
- Reduction % card

## UI states
- **Loading**: shown before evidence files resolve.
- **Missing file**: shown when any required fetch returns non-OK.
- **Malformed data**: shown when shape/types/rows are invalid.
- **Loaded with partial metrics**: shown when optional `p95_latency_ms` is missing.
