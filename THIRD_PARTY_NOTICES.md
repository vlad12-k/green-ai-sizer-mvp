# Third-party and historical notices

The Business Source License applies only to the licensor's covered work.
Dependencies, external data, templates and previously granted rights are excluded.

- **Historical project material:** all copies previously distributed under MIT,
  including v0.1.0 and v0.1.1, retain those rights. The original copyright and MIT
  grant are preserved in [licenses/MIT-legacy.txt](licenses/MIT-legacy.txt).
  `.github/` and `.devcontainer/` scaffolding retain those MIT terms in v0.2.0.
- **Grid data:** `data/grid_intensity_uk_snapshot.csv`,
  `data/grid_intensity_uk_summary.json`, and their dashboard copies contain
  National Energy System Operator / UK Carbon Intensity API forecast data.
  [Source and terms](https://github.com/carbon-intensity/terms),
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Transformations: forecast points exported to CSV, rounded to two decimals,
  and aggregated into minimum/mean/maximum. No endorsement is implied.
- **Gitignore:** `.gitignore` includes the GitHub Node gitignore template,
  licensed under [CC0-1.0](https://github.com/github/gitignore/blob/main/LICENSE).
  It is excluded from BSL; local modifications do not restrict the template.
- **License text:** Business Source License text and trademark belong to MariaDB;
  its notice is retained verbatim in LICENSE.

## Runtime dependencies

| Package | Pinned version | Upstream license |
|---|---|---|
| azure-functions | 1.21.3 | MIT |
| scikit-learn | 1.5.2 | BSD-3-Clause |
| joblib | 1.4.2 | BSD-3-Clause |
| numpy | 1.26.4 | BSD-3-Clause; bundled components have additional notices |
| scipy | 1.13.1 | BSD-3-Clause; bundled components have additional notices |
| threadpoolctl | 3.5.0 | BSD-3-Clause |

These packages are installed from their distributions, not relicensed as project
code. Preserve their installed LICENSE, COPYING, metadata and bundled component
notices when redistributing deployment packages. The same applies to GitHub
Actions, the Python/Node runtimes and devcontainer images under their own terms.
A packaged model references sklearn/joblib classes; it does not change the
licenses of those libraries. No model-training corpus is imported from them.
