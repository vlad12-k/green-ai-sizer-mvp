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

Why: the refresh workflow commits refreshed files directly to `main` using `${{ secrets.GITHUB_TOKEN }}`.

### 2) Branch protection for `main`
In **Settings → Branches**:
- Ensure branch protection permits the refresh workflow token to push direct automation commits.
- Keep required checks as needed for normal development flow.

Why: refresh automation no longer uses PR creation or auto-merge steps.

## Secret safety
- Uses only `${{ secrets.GITHUB_TOKEN }}` for workflow push operations.
- Does not print tokens or secret values in logs.
- Fetch script calls only the public NESO API and stores no credentials.
