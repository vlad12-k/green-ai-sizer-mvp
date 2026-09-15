# GitHub Actions operational settings

This document defines required repository settings for fully automated daily grid-intensity refresh.

## Workflows covered
- `.github/workflows/refresh-grid-intensity.yml`
- `.github/workflows/release-validation.yml`
- `.github/workflows/docs-check.yml`
- `.github/workflows/carbon-budget.yml`

## Required repository settings

### 1) Actions permissions
In **Settings → Actions → General**:
- **Workflow permissions:** prefer read-only defaults; the refresh job explicitly requests its required write permissions.

Why: the refresh workflow needs to push to an automation branch and create/update pull requests.

### 2) Branch protection for `main`
In **Settings → Branches**:
- Keep `main` protected by rulesets that require pull requests (GH013).
- Keep required checks on PRs to `main` (including `carbon-budget` and `release-validation`).

Why: scheduled automation now updates `automation/refresh-grid-intensity`, opens/updates a PR to `main`, and uses auto-merge squash once required checks pass. `carbon-budget` remains on `pull_request` + `push` to `main` (safe default), and should not be switched to `pull_request_target`.

### 3) Repository secret for automation bot token
In **Settings → Secrets and variables → Actions**:
- Add secret **`GH_BOT_TOKEN`** with a fine-grained PAT that has repository access needed to:
  - push to `automation/refresh-grid-intensity`
  - create/edit PRs to `main`
  - enable auto-merge via GitHub CLI

Why: PRs created by `github-actions[bot]` with default `GITHUB_TOKEN` may not reliably trigger required PR checks. Using `GH_BOT_TOKEN` ensures the automation PR receives a real `carbon-budget` status check instead of remaining in “Expected”.

### 4) Pull request settings
In **Settings → General → Pull Requests**:
- Enable **Allow auto-merge**.

Why: the refresh workflow calls `gh pr merge --auto --squash` so merges remain autonomous through branch → PR → auto-merge when direct pushes to `main` are forbidden.

## Refresh automation flow (GH013-safe)
The workflow `.github/workflows/refresh-grid-intensity.yml` runs only on `schedule` and `workflow_dispatch` and performs:
1. Checkout `main`, set up Python 3.11, and run `python scripts/fetch_uk_grid_intensity.py`.
2. Validate canonical outputs, publish all mirrors, and check freshness and carbon budget.
3. Exit cleanly when no tracked files changed.
4. When changed, commit on `automation/refresh-grid-intensity` with bot identity and push that branch.
5. Create or update a PR to `main` with generated UTC and min/avg/max gCO2/kWh from `data/grid_intensity_uk_summary.json`.
6. Request auto-merge squash via GitHub CLI.

If auto-merge is not enabled, the workflow logs:
`Auto-merge is disabled in repo settings. Enable Settings → General → Pull Requests → Allow auto-merge.`

## Secret safety
- Uses `${{ secrets.GH_BOT_TOKEN }}` for checkout/push and GitHub CLI PR operations in the refresh workflow.
- Does not print tokens or secret values in logs.
- Fetch script calls only the public NESO API and stores no credentials.

## v0.2.0 publication contract

The daily/manual refresh workflow is the only automated evidence writer. It
fetches canonical data, validates it, publishes mirrors using
`workbook/evidence.py`, checks freshness and carbon budget, and opens or updates
`automation/refresh-grid-intensity`. Required `carbon-budget` and
`release-validation` checks gate merge. The previous workflow that pushed
mirror commits directly to main has been removed. Manual scenario/probe changes
must run the same publisher and include mirrors in their own reviewed PR.
Invalid fetch results fail before replacing existing evidence. Refresh failure
leaves the last published snapshot available with its original timestamp; the
dashboard labels it historical after 48 hours and release validation fails.
