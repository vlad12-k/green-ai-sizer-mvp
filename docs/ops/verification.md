# Verify fresh data (3 steps)

1. Open the dashboard: `https://vlad12-k.github.io/green-ai-sizer-mvp/` and check the **Last updated** value.
2. Open `docs/evidence/grid_intensity_uk_summary.json` and confirm `generated_utc` matches the dashboard timestamp.
3. Open the refresh workflow page (`.github/workflows/refresh-grid-intensity.yml`) and verify the latest run completed successfully.

## Unified validation

Python 3.11+ and Node.js 22 are required. Run `make verify` for reproducible
offline syntax, JSON, documentation, test, evidence mirror and carbon checks.
Run `make verify-release` before a merge or release; it also requires a grid
snapshot generated within 48 hours. `make check` is a compatibility alias.
The `Release Validation` workflow executes this same release entry point on
PRs and main. Check all CI and CodeQL results against the reviewed commit SHA;
never bypass a failed check or publish from an unmerged branch.
