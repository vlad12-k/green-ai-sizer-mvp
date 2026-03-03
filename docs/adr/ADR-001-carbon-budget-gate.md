# ADR-001 — Carbon Budget Gate in CI

**Status:** Accepted  
**Date:** 2026-03-01  
**Deciders:** AI team, Ops lead, Sustainability lead

---

## Context

AI inference creates operational emissions that are invisible unless explicitly measured and governed. Without an automated enforcement point, workbook estimates can become stale or be bypassed during merges. The team needed a lightweight, reproducible gate that blocks merges when the emissions budget is exceeded.

## Decision

Implement a **Carbon Budget Gate** as a required GitHub Actions check on every pull request and push to `main`. The check runs `workbook/calc_co2e.py` against a configurable budget (default 200 gCO₂e / 1k requests) and exits non-zero on budget breach.

Evidence source: `workbook/appendix-d-baseline-improved.csv`  
Calculator: `workbook/calc_co2e.py`  
Workflow: `.github/workflows/carbon-budget.yml`

## Rationale

- Enforces the budget at the merge gate, not just in documentation.
- Uses existing Python tooling; no new dependencies required.
- Results appear in the GitHub Actions run summary for visibility.
- The gate is reproducible locally: `python workbook/calc_co2e.py 200`.

## Consequences

- Any PR that increases the improved scenario's gCO₂e/1k above the budget will fail CI.
- Budget threshold changes require a deliberate PR and review.
- Workbook CSV changes trigger a re-evaluation on the next CI run.

## Alternatives considered

- **No gate (documentation only):** rejected — no enforcement; estimates can drift.
- **Separate monitoring service:** rejected — adds cost and complexity; not required at this stage.
