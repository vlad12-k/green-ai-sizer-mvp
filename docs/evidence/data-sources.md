# Scenario and Data Evidence — Data Sources (Grid Carbon Intensity)

## UK Grid Carbon Intensity (real-world data)
**Source:** NESO / UK Carbon Intensity API (public endpoint, no API key required).  
**Endpoint used:** `GET https://api.carbonintensity.org.uk/intensity/date`  
**Data window:** last 24 hours (half-hourly records).  
**Field used:** `intensity.forecast` (gCO2/kWh).

## How the data is used in the workbook
- A snapshot is stored in `data/grid_intensity_uk_snapshot.csv` for transparency and reproducibility.
- A summary file is stored in `data/grid_intensity_uk_summary.json` containing min/avg/max.
- The workbook uses `avg_g_per_kwh` as the default reporting value for `grid_intensity_g_per_kwh`.
- Sensitivity analysis is performed using `min_g_per_kwh` and `max_g_per_kwh` to show best/worst-case CO2e intensity outcomes.

## Limitations
- Grid intensity varies by time and location; values represent the UK national grid mix at the time of measurement.
- Forecast intensity is used for consistency with the API output; marginal emissions may differ in practice.

---

### D1. UK grid carbon intensity (real-world data)
**Purpose:** Provide a real-world grid intensity value used by the workbook CO₂e calculator and CI gate.

**Primary source (API):**
- National Grid ESO Carbon Intensity API (UK)

**Evidence stored in this repository:**
- `data/grid_intensity_uk_snapshot.csv` — raw snapshot exported by the fetch script
- `data/grid_intensity_uk_summary.json` — derived summary used for traceability (includes the value used in the workbook)

**How the data is collected (reproducible):**
- Script: `scripts/fetch_uk_grid_intensity.py`
- Automated refresh: GitHub Actions workflow `refresh-grid-intensity.yml` (scheduled + manual trigger)

**Value used in the workbook:**
- The value written into `data/scenario-baseline-improved.csv` (`grid_intensity_g_per_kwh`) must match the current snapshot/summary evidence.

---

### D2. Routing & cache performance evidence (live endpoint probe)
**Purpose:** Record observed routing and caching behaviour used to populate the “improved” scenario metrics.

**Evidence stored in this repository:**
- `scripts/probe_endpoint.py` — reproducible probe script (HTTP POST loop)
- `scripts/probe_run_summary.json` — captured run summary (cache hit rate, small route rate, latency metrics, avg Wh/request)

**How to reproduce:**
- Requires a local `.env` containing the deployed Function URL (including `?code=...`) and must not be committed.
- Run:
  - `python scripts/probe_endpoint.py > scripts/probe_run_summary.json`

**Mapping to workbook:**
The following fields in `data/scenario-baseline-improved.csv` (scenario = `improved`) are updated from `probe_run_summary.json`:
- `cache_hit_rate`
- `small_route_rate`
- `avg_latency_ms`
- `p95_latency_ms`

---

### D3. Workbook inputs used by the CI Carbon Budget Gate
**Purpose:** Show exactly which inputs drive the CI “PASS/FAIL” result.

**Evidence stored in this repository:**
- `data/scenario-baseline-improved.csv` — baseline vs improved scenario inputs
- `workbook/calc_co2e.py` — calculator used locally and in CI

**Reproducible check:**
- `python workbook/calc_co2e.py 200`

Expected outcome:
- Baseline and improved gCO₂e per 1k requests are printed
- CI should report **PASS** when improved is within budget
