# System boundary

The carbon engine estimates scenario emissions from assumed request volumes,
cache/routing rates, energy per route and the canonical UK grid forecast mean.
It does not measure the energy of a running LLM or the Azure Function.

The scenario assumes 0.2 Wh per small request and 2.0 Wh per large request.
Cached requests contribute zero energy in the workbook model; the optional
runtime uses a separate simulated 0.02 Wh cache value. These models must not be
presented as equivalent measured telemetry. Historical probe rates remain
scenario inputs, not evidence of Router v2 production behavior.

Excluded: embodied emissions, device energy, network and logging overhead,
provider-specific hardware utilization, data-centre PUE, and Azure overhead.
The resulting estimate is incomplete; no precise real-world savings are claimed.

Use the current snapshot minimum/maximum to explore grid sensitivity separately.
The release gate always uses the canonical mean. Explicit sensitivity-analysis
rows and production-calibrated energy measurements remain future work.
