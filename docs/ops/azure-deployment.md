# Optional Azure simulation deployment

Deployment is an explicit `workflow_dispatch` operation from `main`. Pushes and
pull requests do not deploy. Selecting another branch skips the build and deploy
jobs. The workflow checks out its immutable event commit, installs pinned
validation dependencies, and runs `make verify-release` before packaging `app/`.
The deploy job depends on this successful build and downloads only that run's
artifact. Concurrent production deployments are serialized.

Before dispatch, review the main SHA and require successful Release Validation,
Carbon Budget Gate, docs checks, and CodeQL for that SHA. Record the resulting
workflow run and deployed commit. A failed validation must be fixed through a PR;
do not rerun deployment from an unreviewed branch or bypass the gate.

The existing Azure OIDC secret names and app target are retained. No new
GitHub environment is introduced, so the existing OIDC subject remains compatible.
The repository remains fully usable offline without Azure credentials. This
workflow deploys a simulation, not hosted LLM inference. Workflow validation
alone does not prove the live endpoint's health; verify it separately after any
operator-requested deployment, using a function key kept out of logs.
