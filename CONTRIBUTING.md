# Contributing

## Branching and PR workflow
- Work on `dev` (or a short-lived feature branch from `dev`).
- Open a Pull Request into `main`.
- Merging into `main` requires required checks to pass (Carbon Budget Gate + CodeQL).

## Evidence discipline
If you change workbook inputs or assumptions:
- Update `workbook/appendix-d-baseline-improved.csv`
- Ensure the Carbon Budget Gate summary reflects the updated CO₂e metrics
- Update any relevant appendix under `/docs` (boundary, KPIs, risks)

## Commit messages
Use clear, action-oriented messages:
- `docs: ...`, `ci: ...`, `feat: ...`, `chore: ...`
