# GitHub Actions operational settings

This document defines required repository settings for fully automated daily grid-intensity refresh.

## Workflows covered
- `.github/workflows/refresh-grid-intensity.yml`
- `.github/workflows/sync-dashboard-evidence.yml`
- `.github/workflows/docs-check.yml`
- `.github/workflows/carbon-budget.yml`

## Required repository settings

### 1) Actions permissions
In **Settings → Actions → General**:
- **Workflow permissions:** `Read and write permissions`

Why: the refresh workflow needs to push to an automation branch and create/update pull requests using `${{ secrets.GITHUB_TOKEN }}`.

### 2) Branch protection for `main`
In **Settings → Branches**:
- Keep `main` protected by rulesets that require pull requests (GH013).
- Keep required checks on PRs to `main` (including `carbon-budget`).

Why: scheduled automation now updates `automation/refresh-grid-intensity`, opens/updates a PR to `main`, and uses auto-merge squash once required checks pass.

### 3) Pull request settings
In **Settings → General → Pull Requests**:
- Enable **Allow auto-merge**.

Why: the refresh workflow calls `gh pr merge --auto --squash` so merges remain autonomous even when direct push to `main` is forbidden.

## Refresh automation flow (GH013-safe)
The workflow `.github/workflows/refresh-grid-intensity.yml` runs only on `schedule` and `workflow_dispatch` and performs:
1. Checkout `main`, set up Python 3.11, and run `python scripts/fetch_uk_grid_intensity.py`.
2. Ensure canonical outputs are present and copy summary JSON to `docs/evidence/`.
3. Exit cleanly when no tracked files changed.
4. When changed, commit on `automation/refresh-grid-intensity` with bot identity and push that branch.
5. Create or update a PR to `main` with generated UTC and min/avg/max gCO2/kWh from `data/grid_intensity_uk_summary.json`.
6. Request auto-merge squash via GitHub CLI.

If auto-merge is not enabled, the workflow logs:
`Auto-merge is disabled in repo settings. Enable Settings → General → Pull Requests → Allow auto-merge.`

## Secret safety
- Uses only `${{ secrets.GITHUB_TOKEN }}` for workflow push operations.
- Does not print tokens or secret values in logs.
- Fetch script calls only the public NESO API and stores no credentials.
