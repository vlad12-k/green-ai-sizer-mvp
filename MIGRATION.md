# Migration mapping: appendix naming → product naming

This migration keeps evidence files intact while replacing appendix-style naming with product-grade structure.

## Path mapping

| Old path | New path |
|---|---|
| `workbook/appendix-d-baseline-improved.csv` | `data/scenario-baseline-improved.csv` |
| `docs/evidence/appendix-d-baseline-improved.csv` | `docs/evidence/scenario-baseline-improved.csv` |
| `docs/appendix-a-architecture.md` | `docs/architecture/system-architecture.md` |
| `docs/appendix-c-boundary.md` | `docs/governance/system-boundary.md` |
| `docs/appendix-d-data-sources.md` | `docs/evidence/data-sources.md` |
| `docs/appendix-e-raci.md` | `docs/governance/raci.md` |
| `docs/appendix-f-kpis.md` | `docs/governance/kpis.md` |
| `docs/appendix-g-risk-register.md` | `docs/governance/risk-register.md` |
| `docs/controls.md` | `docs/governance/controls.md` |
| `docs/runbook.md` | `docs/governance/runbook.md` |

## Notes

- File history is preserved via `git mv`.
- Dashboard and workflow references were updated to point to new paths.
- No core calculation logic or product behavior was changed beyond path/reference updates.
