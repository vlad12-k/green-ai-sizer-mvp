# green-ai-sizer-mvp

Azure-led **Responsible AI Sizing** MVP for climate-critical services: **routing + caching + inference governance** plus a **Carbon Budget Gate** in GitHub Actions.

## Why this matters
Heatwaves and grid volatility increase operational pressure on digital services. AI inference can become an “always-on” baseline load and push carbon emissions upward unless demand is governed.

## What this MVP demonstrates
- **Routing (small-first)**: simple requests go to a “small” path, complex ones escalate to a “large” path.
- **Caching**: repeat requests are served from cache to reduce compute.
- **Inference governance**: budget mindset (quotas/policies) represented as CI checks.
- **Evidence**: baseline vs improved metrics + CO₂e workbook.

## Architecture (high-level)
Gateway → Orchestrator (routing + cache check) → Small path / Large path → Observability → Workbook (CO₂e)

> Azure implementation will be added in the practical phase with minimal cost.

## Repo structure
- `app/` — MVP service code (added in Phase 2)
- `docs/` — appendices (C/E/F/G) and architecture diagram notes
- `workbook/` — Appendix D (baseline vs improved) + CO₂e calculator
- `.github/workflows/` — Carbon Budget Gate (GitHub Actions)

## Appendices (mapped to the report)
- **Appendix C**: Assumptions & system boundary (`docs/appendix-c-boundary.md`)
- **Appendix D**: Carbon calculation workbook (`workbook/appendix-d-baseline-improved.csv`)
- **Appendix E**: Stakeholders + RACI (`docs/appendix-e-raci.md`)
- **Appendix F**: KPI set (`docs/appendix-f-kpis.md`)
- **Appendix G**: Risk register (`docs/appendix-g-risk-register.md`)

## How the Carbon Budget Gate works
A GitHub Action reads the workbook CSV and computes:
- **gCO₂e per 1,000 requests**
If the value exceeds the defined budget, the workflow fails (simulating governance).

## Status
- Phase 1 (GitHub): in progress ✅
- Phase 2 (Azure MVP test + metrics): next
