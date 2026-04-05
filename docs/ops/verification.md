# Verify fresh data (3 steps)

1. Open the dashboard: `https://vlad12-k.github.io/green-ai-sizer-mvp/` and check the **Last updated** value.
2. Open `docs/evidence/grid_intensity_uk_summary.json` and confirm `generated_utc` matches the dashboard timestamp.
3. Open the refresh workflow page (`.github/workflows/refresh-grid-intensity.yml`) and verify the latest run completed successfully.
