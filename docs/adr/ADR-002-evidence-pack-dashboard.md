# ADR-002 — Evidence pack and static monitoring dashboard

**Status:** Accepted  
**Date:** 2026-03-01  
**Deciders:** AI team, Sustainability lead

---

## Context

Stakeholders and auditors need to verify that reported emissions figures are traceable to specific inputs and assumptions. A dashboard helps communicate current KPI values without requiring access to GitHub Actions logs. The team needed an approach that adds no Azure cost and no build toolchain.

## Decision

Maintain an **evidence pack** of appendix-style Markdown documents under `docs/`, and publish a **static GitHub Pages dashboard** (`docs/index.html`, `docs/styles.css`, `docs/app.js`) that reads committed JSON evidence files at page load.

Evidence sources used by the dashboard:

- `workbook/appendix-d-baseline-improved.csv`
- `data/grid_intensity_uk_summary.json`
- `scripts/probe_run_summary.json`

## Rationale

- Pure static HTML/CSS/JS: no build tools, no CDN, no external API calls.
- Data is sourced exclusively from committed evidence files; no invented values.
- GitHub Pages hosting is free and requires no new infrastructure.
- The dashboard includes a governance view (controls register, evidence links) alongside KPI charts.

## Consequences

- Dashboard values reflect the last committed state of evidence files, not real-time Azure telemetry.
- Grid intensity values are refreshed daily by the existing `refresh-grid-intensity.yml` workflow.
- A `Last updated` indicator reflects the `generated_utc` field in the grid intensity JSON.

## Alternatives considered

- **Azure Application Insights dashboard:** rejected — adds cost; violates "no new Azure resources" constraint.
- **Build-tool-based SPA:** rejected — introduces toolchain complexity and security surface.
