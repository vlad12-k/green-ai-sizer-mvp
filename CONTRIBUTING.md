# Contributing

Thanks for your interest in improving this project.

This repository is maintained as a **governance-first evidence pack**: changes must be reproducible, reviewable, and traceable to workbook inputs and documented assumptions.

---

## 1) Development workflow (branches & PRs)

### Branch model
- Default development happens on `dev`.
- Use short-lived branches from `dev` for focused changes:
  - `docs/...`, `ci/...`, `feat/...`, `fix/...`

### Pull requests
- Open PRs into `main`.
- `main` is protected: direct commits are not allowed.
- A PR can be merged only when required checks pass (e.g., **Carbon Budget Gate**, **CodeQL**).

### Merge strategy
Prefer **Squash and merge** for small changes (keeps history clean), unless a PR contains multiple logically independent commits.

---

## 2) Required checks (quality gate)

Before merge, the following must pass:
- **Carbon Budget Gate** (CO₂e budget enforcement)
- **CodeQL** (code scanning), if enabled

If a PR changes workbook inputs or calculator logic, reviewers should verify the updated values appear in the GitHub Actions run summary.

---

## 3) Evidence discipline (workbook + appendices)

This project treats evidence as a first-class artefact.

### When you change workbook inputs
If you edit:
- `workbook/appendix-d-baseline-improved.csv`

You must:
1. Ensure the calculator still runs:
   - `python workbook/calc_co2e.py 200`
2. Confirm CI summary shows updated values (baseline, improved, reduction).
3. Update related appendix documentation in `/docs` where needed:
   - boundary/assumptions (Appendix C)
   - KPI definitions (Appendix F)
   - risks and mitigations (Appendix G)

### When you change calculator logic
If you edit:
- `workbook/calc_co2e.py`

You must:
- maintain clear validation errors and stable outputs
- keep the Step Summary readable (results + budget + reduction)

---

## 4) Security & secrets policy

Do not commit:
- API keys, tokens, credentials
- `.env` files containing secrets
- real customer/clinical data

Use GitHub repository secrets if integrations are added later (Azure stage).

---

## 5) Commit message conventions

Use short, action-oriented messages:
- `docs: ...` documentation and appendices
- `ci: ...` GitHub Actions / workflow changes
- `feat: ...` new functionality
- `fix: ...` bug fixes
- `chore: ...` maintenance / refactors

Examples:
- `docs: add sensitivity scenario rows to Appendix D`
- `ci: enforce carbon budget via workflow`
- `fix: handle empty rows in workbook CSV`

---

## 6) Definition of Done (DoD)

A change is “done” when:
- [ ] The PR has a clear description and scope
- [ ] Required checks pass
- [ ] Workbook/calculator outputs remain reproducible
- [ ] Documentation is updated where it affects assumptions, KPIs, or risks
- [ ] Changelog is updated for user-visible changes

---

## 7) Releases & changelog

- Changes intended for a release should be recorded in `CHANGELOG.md` under **[Unreleased]**.
- Tag releases using Semantic Versioning (e.g., `v0.2.0`).
- Release notes should summarise user-visible changes and verification steps.
