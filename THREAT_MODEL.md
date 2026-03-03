# Threat model

This document applies a lightweight STRIDE analysis to the Green AI Sizer MVP system. It covers the assets under management, relevant threats, and the controls or mitigations in place.

---

## Assets

| Asset | Description | Location |
|---|---|---|
| Workbook CSV | Scenario inputs driving the CI carbon budget decision | `workbook/appendix-d-baseline-improved.csv` |
| Azure Function key | Authentication credential for the live endpoint | Local `.env` only (never committed) |
| Grid intensity data | Real-world UK grid data used in calculations | `data/grid_intensity_uk_summary.json` |
| Probe run summary | Evidence of endpoint behaviour committed to repo | `scripts/probe_run_summary.json` |
| GitHub repository | Version control, CI pipelines, branch protections | GitHub |
| GitHub Actions workflows | Automated CI and data refresh pipelines | `.github/workflows/` |

---

## STRIDE threat table

| ID | Asset | Threat category | Threat | Likelihood | Impact | Mitigation | Residual risk |
|---|---|---|---|---|---|---|---|
| T-01 | Azure Function key | **Information Disclosure** | Function key committed to repository (in code, config, or `.env` file) | Medium | High — enables unauthorised Azure calls and cost | `.gitignore` excludes `.env`; `SECURITY.md` policy; CodeQL scans for secrets; never print key in logs | Low (if policy followed) |
| T-02 | Azure Function key | **Elevation of Privilege** | Leaked key used to exfiltrate prompt data or abuse the endpoint | Low | Medium — no PII in prompts; cost exposure limited by Function App budget | Key rotation procedure in `SECURITY.md`; Function App can be stopped immediately | Low |
| T-03 | Workbook CSV | **Tampering** | Malicious or accidental change to scenario inputs bypasses the budget gate | Low | High — CI would produce wrong PASS/FAIL | Branch protection on `main`; PR review required; git history provides audit trail | Low |
| T-04 | GitHub Actions workflows | **Tampering** | Workflow modified to suppress budget gate failure or to exfiltrate secrets | Low | High | Branch protection; PR review required; no secrets printed in logs | Low |
| T-05 | Grid intensity data | **Tampering** | Automated refresh commits manipulated grid intensity values | Low | Medium — affects calculation results; would surface in evidence review | Refresh workflow commits via a controlled bot account; data sourced from public NESO API with no authentication; spot-check during quarterly review | Low |
| T-06 | Grid intensity data | **Denial of Service** | NESO API unavailable; refresh workflow fails | Medium | Low — stale data; CI continues using last committed values | Workflow designed to exit gracefully if API is unavailable; stale data is clearly timestamped | Low |
| T-07 | GitHub repository | **Denial of Service** | GitHub Actions rate limiting or outage delays CI | Low | Low — no production dependency on CI completing in real time | Monitored via GitHub status; no mitigation needed at MVP stage | Low |
| T-08 | Probe run summary | **Repudiation** | Probe output committed without a clear provenance trail | Low | Low — evidence value is reduced | Probe script and methodology documented in `docs/appendix-d-data-sources.md`; commit message includes "probe" keyword | Low |

---

## Out of scope

- End-user device threats (browser, network).
- Azure infrastructure security (managed by Microsoft; covered by shared responsibility model).
- Supply chain attacks on Python dependencies (addressed by Dependabot and CodeQL, where enabled).

---

## Review

This threat model should be reviewed:

- On any change to the Azure Function deployment or key management approach.
- When new data sources or external integrations are added.
- Annually as part of the governance review cycle.

Owner: Security lead. Evidence: `SECURITY.md`, `docs/controls.md` (C-05, C-08).
