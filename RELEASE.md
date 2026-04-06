# Release guide

## Versioning

This project follows **Semantic Versioning (SemVer)**:

- **MAJOR**: incompatible changes
- **MINOR**: backward-compatible feature additions
- **PATCH**: backward-compatible fixes and documentation/process improvements

## Release checklist

- [ ] `make check` passes
- [ ] `python workbook/calc_co2e.py 200` passes
- [ ] Carbon Budget Gate workflow is green
- [ ] Refresh grid-intensity workflow is green
- [ ] Dashboard loads on GitHub Pages
- [ ] `Last updated` in dashboard reflects fresh `generated_utc` from `docs/evidence/grid_intensity_uk_summary.json`
- [ ] Latest refresh automation PR was created and merged successfully

## Automation proof artifacts

A release should be backed by three observable artifacts:

1. **GitHub Actions run**: successful `refresh-grid-intensity.yml` execution.
2. **Merged automation PR**: `data: refresh UK grid intensity snapshot (auto)` merged to `main`.
3. **Updated evidence**: refreshed timestamp/values in `docs/evidence/grid_intensity_uk_summary.json` visible on GitHub Pages dashboard.

