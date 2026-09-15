# System architecture

Green AI Sizer separates offline evidence calculation from an optional request
simulation. The product boundary is described in the root README.

## Evidence path

NESO forecast API → canonical snapshot CSV → validated summary → carbon engine
and published dashboard mirrors. Scenario workload/energy assumptions are read
from `data/scenario-baseline-improved.csv`. Its old grid value is historical;
both active calculations use `avg_g_per_kwh` from the canonical summary.

The carbon formula is computed requests × weighted Wh per request / 1000 ×
grid intensity, normalized to 1,000 incoming requests. Cached requests are
assumed zero energy in this scenario model; the runtime's simulated cache
energy of 0.02 Wh is not included. Neither is measured hardware telemetry.

`workbook/evidence.py` validates snapshot/summary agreement and publishes three
mirrors to `docs/evidence/`. CI checks byte equality and release freshness. The
daily automation proposes all changes through a PR. Pages reads committed
mirrors only and labels snapshots older than 48 hours as historical.

## Request path

`app/orchestrator` validates JSON and invokes Router v2. Explicit sensitivity
policy rejects a request. Complexity rules, simple-request rules and a TF-IDF /
logistic regression model choose small or large with conservative fallback.
The endpoint returns a decision object and explicitly simulated telemetry.
There is no provider invocation, real cache or measured LLM response quality.
See the [model card](../router-model-card.md).

## Validation and deployment

`make verify` runs the shared offline contract; `make verify-release` adds
freshness. Required `carbon-budget` and `release-validation` checks protect main.
An operator can dispatch the optional Azure workflow from main; its build
runs the release contract before packaging the same commit and its notices.
Deploy depends on that validated artifact. See [deployment](../ops/azure-deployment.md).

The static dashboard and all offline tests need no Azure account or API key.
Live deployment status must be verified from its run and endpoint separately.
