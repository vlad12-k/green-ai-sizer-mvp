# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-04-06

### Added
- CI **Carbon Budget Gate** workflow enforcing `python workbook/calc_co2e.py 200` on pull requests and main pushes.
- Evidence-driven GitHub Pages dashboard consuming committed files from `docs/evidence/`.
- Daily UK grid-intensity refresh automation that updates evidence via PR + auto-merge using `GH_BOT_TOKEN`.
- Test and smoke-check validation via `make check`.
- Governance and operations documentation under `docs/governance/` and `docs/ops/`.

