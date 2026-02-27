## Release scope
This is the first tagged portfolio release focused on **governance and evidence artefacts** for the Topic 5 “Responsible AI Sizing” case study. It packages the minimum reproducible layer needed to support carbon-aware decision-making (routing/caching/inference control) and to demonstrate auditability of assumptions and KPIs.

## What’s included
### Governance automation (CI)
- **Carbon Budget Gate** (GitHub Actions): computes and enforces a **CO₂e budget per 1,000 requests** based on the workbook inputs and fails the pipeline when the threshold is exceeded.
- **Run summary output**: surfaces baseline vs improved CO₂e intensity and an estimated reduction directly in the workflow summary for reviewer traceability.

### Evidence pack (appendices)
- `/docs` — report appendices scaffolding:
  - **Appendix C**: system boundary + modelling assumptions (what is included/excluded and why).
  - **Appendix E**: stakeholder mapping + RACI to support governance ownership (budgets, policies, incident exceptions).
  - **Appendix F**: KPI definitions and reporting cadence (gCO₂e/1k requests, cache hit rate, routing %, p95 latency, feature-level demand signals).
  - **Appendix G**: risk register (rebound, privacy, lock-in, heatwave/outage, monitoring overhead) with mitigation intent.
- `/workbook` — calculation artefacts:
  - `appendix-d-baseline-improved.csv` (baseline vs improved scenarios; intended for sensitivity expansion).
  - `calc_co2e.py` (calculator used by CI gate).

## Critical notes (limitations)
- **This release does not claim production-grade carbon accounting.** The calculator is a transparent, scenario-driven method designed for coursework evidence and governance demonstration.
- **Energy-per-request inputs are proxies** and must be replaced or triangulated with measured telemetry (planned Azure MVP) or cited benchmarks.
- **Boundary exclusions** (e.g., embodied hardware emissions, full data centre PUE effects, end-user devices) are documented in Appendix C and should be revisited if the solution scope expands.

## Verification (reproducible checks)
1. Run locally (or in Codespaces):
   - `python workbook/calc_co2e.py 200`
2. Confirm GitHub Actions:
   - Carbon Budget Gate run passes and the summary displays CO₂e/1k and reduction.
3. Inspect evidence artefacts:
   - `/docs` appendices and `/workbook` CSV align with the report structure and system boundary.

## Next steps (portfolio maturity)
- Introduce **PR-only workflow** and protect `main` (require Carbon Budget Gate status check).
- Add **Codespaces devcontainer** for one-click reproducibility and a standardised toolchain (Python + Node).
- Add **GitHub Pages UI** to visualise baseline vs improved KPIs and sensitivity scenarios.
- Azure MVP (later, minimal cost): collect **real routing/cache/latency** metrics and update Appendix D with measured values + sensitivity analysis.
