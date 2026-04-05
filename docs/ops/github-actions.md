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
- **Allow GitHub Actions to create and approve pull requests:** enabled

Why: the refresh workflow commits to `automation/refresh-grid-intensity`, opens/updates a PR, posts status comments, and attempts auto-merge.

### 2) Pull request auto-merge
In **Settings → General**:
- **Allow auto-merge:** enabled

Why: the refresh workflow enables auto-merge on the generated PR after checks pass.

### 3) Branch protection for `main`
In **Settings → Branches**:
- Require pull request before merge
- Require status checks to pass before merge (include docs/integrity and any required security checks)

Why: automation should merge only after required checks are green.

## Fallback behavior when auto-merge is blocked
If repository settings prevent auto-merge (or branch rules reject it), the workflow still:
- pushes refreshed files to `automation/refresh-grid-intensity`
- opens/updates the PR
- posts a fallback status comment on the PR

This preserves end-to-end reliability even when auto-merge cannot be enabled.

## Secret safety
- Uses only `${{ secrets.GITHUB_TOKEN }}` for GitHub API operations.
- Does not print tokens or secret values in logs.
- Fetch script calls only the public NESO API and stores no credentials.
