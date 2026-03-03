# Controls register

This document maps each governance control objective to the specific control implemented, the evidence artefact that demonstrates it, and the review cadence.

---

## Controls

| # | Control objective | Control | Evidence artefact | Review cadence |
|---|---|---|---|---|
| C-01 | CO₂e per 1k requests stays within the approved budget | Carbon Budget Gate — required CI check on every PR and push to `main` | `.github/workflows/carbon-budget.yml` run summary; `workbook/calc_co2e.py` exit code | Every PR; monthly trend review |
| C-02 | Budget inputs are traceable, versioned, and auditable | Workbook scenario CSV committed under version control; changes require a reviewed PR | `workbook/appendix-d-baseline-improved.csv` git history | On every change; quarterly audit |
| C-03 | Grid intensity values reflect real-world UK national grid data | Daily automated refresh via GitHub Actions; data sourced from public NESO API | `data/grid_intensity_uk_summary.json`; `data/grid_intensity_uk_snapshot.csv` | Daily (automated); monthly spot-check |
| C-04 | Endpoint routing and caching behaviour is evidenced | Versioned probe run summary committed to repository | `scripts/probe_run_summary.json`; `scripts/probe_endpoint.py` | Per evidence refresh (at most weekly) |
| C-05 | Secrets and credentials are never committed | `.gitignore` excludes `.env` and `.env.*`; SECURITY.md policy; no URLs with `?code=` in committed files | `.gitignore`; `SECURITY.md`; CodeQL scans | Continuous (pre-commit awareness); quarterly review |
| C-06 | System boundary and assumptions are documented | Appendix C boundary document maintained under version control | `docs/appendix-c-boundary.md` | On assumption change; quarterly review |
| C-07 | Data sources are documented and reproducible | Appendix D data sources document; fetch script committed | `docs/appendix-d-data-sources.md`; `scripts/fetch_uk_grid_intensity.py` | On source change; quarterly review |
| C-08 | Risks are identified and mitigations are documented | Risk register maintained and reviewed | `docs/appendix-g-risk-register.md` | Quarterly risk review |
| C-09 | KPIs are defined and reportable | KPI definitions and reporting cadence documented | `docs/appendix-f-kpis.md` | Quarterly or on KPI change |
| C-10 | Stakeholder accountability is defined | RACI table maintained | `docs/appendix-e-raci.md` | Annually or on team change |
| C-11 | Architecture decisions are recorded and justified | ADR set under `docs/adr/` | `docs/adr/ADR-001-carbon-budget-gate.md`, `ADR-002-evidence-pack-dashboard.md`, `ADR-003-secret-handling.md` | On architectural change |
| C-12 | Operator procedures are documented | Runbook covering validation, key rotation, evidence refresh, spend pause | `docs/runbook.md` | Quarterly review; on procedure change |

---

## Review owners

| Cadence | Owner | Artefacts covered |
|---|---|---|
| Every PR | Reviewer (AI team / Ops) | C-01 |
| Daily (automated) | GitHub Actions bot | C-03 |
| Monthly | Sustainability lead | C-01, C-02, C-04 trend |
| Quarterly | Governance owner (Exec sponsor) | C-02, C-05 through C-12 |
| On incident | Security lead | C-05 |

---

## Evidence file index

| File | Controls | Notes |
|---|---|---|
| `workbook/appendix-d-baseline-improved.csv` | C-01, C-02 | Primary budget input |
| `workbook/calc_co2e.py` | C-01 | Calculator logic; must not be changed without review |
| `data/grid_intensity_uk_summary.json` | C-03 | Auto-refreshed; `generated_utc` field provides timestamp |
| `data/grid_intensity_uk_snapshot.csv` | C-03 | Raw 24 h readings |
| `scripts/probe_run_summary.json` | C-04 | Updated on deliberate probe run |
| `.gitignore` | C-05 | Excludes `.env`, `.env.*` |
| `SECURITY.md` | C-05 | Policy + rotation procedure |
| `THREAT_MODEL.md` | C-05, C-08 | STRIDE table |
| `docs/appendix-c-boundary.md` | C-06 | System boundary and assumptions |
| `docs/appendix-d-data-sources.md` | C-07 | Data provenance |
| `docs/appendix-g-risk-register.md` | C-08 | Risk register |
| `docs/appendix-f-kpis.md` | C-09 | KPI definitions |
| `docs/appendix-e-raci.md` | C-10 | RACI |
| `docs/adr/` | C-11 | Architecture decision records |
| `docs/runbook.md` | C-12 | Operator runbook |
