# v0.2.0 provenance audit

Audit date: 2026-09-15. Baseline: `bdcf99dd6e8f9712f8f285722d0439ba5ee0ec25`.
Scope: all fetched Git refs, author/co-author history, tracked-file origins,
repository license/source notices, text assets, model provenance and installed
runtime dependency license metadata. The original MIT grant is preserved in
`licenses/MIT-legacy.txt`; no old tags or releases are rewritten.

## Findings and disposition

| Material | Evidence | Disposition |
|---|---|---|
| Project code and docs | Git author history identifies Vladyslav Kononov; GitHub contributor API identifies vlad12-k as the only human contributor | BSL applies to the licensor's v0.2.0+ work; previous MIT grants remain valid |
| Copilot-assisted work | Copilot and copilot-swe-agent bot commits and co-author trailers are present | Preserve history and original MIT notice; bot attribution is not proof of independent human ownership or originality |
| Automation | github-actions bot changes contain generated evidence | Preserve source attribution and data terms |
| Grid snapshot and summary | Fetch code identifies NESO Carbon Intensity API; upstream terms identify CC BY 4.0 | Exclude from BSL; preserve attribution, license link and transformation description |
| Gitignore template | Content closely matches github/gitignore Node template, with version differences and local Python additions; upstream is CC0-1.0 | Treat as third-party template, excluded from BSL |
| Workflow/devcontainer scaffolding | Azure-generated workflow history and standard configuration patterns | Retain historical MIT terms for `.github/` and `.devcontainer/`; no exclusive authorship claim |
| Router model | Only tracked binary asset; v2 rebuilt from project-authored synthetic training CSV with pinned sklearn/joblib | Project model parameters covered by BSL; embedded library objects remain under their upstream terms |
| Dependencies and Actions | Referenced packages/actions are external; no vendored library source or bundled fonts/images found | Their own licenses/notices remain in force; BSL does not relicense them |

No other human contributor, separately attributed copied application code,
vendored library tree, third-party media, or additional license header was found
in the inspected repository. The author identity and copyright notice agree on
Vladyslav Kononov. The maintainer confirmed the licensing parameters and stated
that the original code is believed to be theirs; Git metadata cannot establish
unrecorded provenance or provide a legal warranty of originality.

## Scope decision

The repository evidence audit is complete. No identified third-party component
is assigned to the licensor. The migration preserves all previous MIT grants
and explicitly excludes external data, dependency code, gitignore and retained
MIT scaffolding. Unknown future contributions require a provenance review and
explicit permission before being included in the BSL-covered work. Do not infer
assignment or relicensing consent solely from submitting a pull request.

## References

- [BSL 1.1 terms](https://mariadb.com/bsl11/)
- [Unmodified SPDX license text](https://github.com/spdx/license-list-data/blob/main/text/BUSL-1.1.txt)
- [NESO API terms and data license](https://github.com/carbon-intensity/terms)
- [Gitignore template license](https://github.com/github/gitignore/blob/main/LICENSE)
