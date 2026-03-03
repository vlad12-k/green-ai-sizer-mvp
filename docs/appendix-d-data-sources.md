# Appendix D — Data Sources (Grid Carbon Intensity)

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

## SECURITY.md 

```markdown
# Security policy

This repository is a governance-first evidence pack. Security and data discipline are treated as first-class requirements.

## Secrets and credentials
Do not commit any of the following:
- Azure Function keys, access tokens, client secrets, credentials
- `.env` files containing secrets (this repo ignores `.env` by design)
- customer / clinical / personal data

Store the deployed Azure Function URL (including `?code=...`) locally in a `.env` file.

## Key rotation (Azure Functions)
If a function key is exposed, rotate it immediately:
Azure Portal → Function App → Functions → `orchestrator` → Function Keys → regenerate the affected key.

After rotation, update your local `.env`.

## Dependency and code scanning
- Keep GitHub Actions workflows enabled.
- Use Dependabot alerts and CodeQL (if enabled) for continuous scanning.

## Data policy
This repository may include:
- public grid carbon intensity snapshots from official/public APIs
- synthetic prompts for routing tests

It must not include sensitive operational or personal data.
