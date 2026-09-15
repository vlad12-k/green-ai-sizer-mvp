# Evidence sources and limitations

## Grid forecast

Source: [NESO / UK Carbon Intensity API](https://api.carbonintensity.org.uk/intensity/date).
The fetcher stores half-hourly `intensity.forecast` values and an aggregate
summary. The actual returned timestamps define the window; it is not assumed
to be a rolling last-24-hour measurement. Data retains its upstream terms and
CC BY 4.0 attribution; see the root THIRD_PARTY_NOTICES.md.

The canonical snapshot and summary are in `data/`. The engine and dashboard use
the validated summary mean, not the historical grid field in the scenario CSV.
Grid emissions are a national forecast proxy, not marginal or provider-specific
emissions. Refresh automation publishes the mirrors in a gated PR.

## Historical simulation probe

`scripts/probe_run_summary.json` is retained historical endpoint evidence.
Routing/cache/latency/energy fields describe a simulation; they do not measure
LLM quality or hardware energy. The old probe is not a Router v2 benchmark.
Missing p95 is shown as unavailable. Its age is independent of grid freshness.

Scenario cache/routing values are explicit assumptions informed by that earlier
probe. No claim is made that current runtime routing rates equal those inputs.
To capture a new probe, configure the endpoint outside version control and
review the collected metrics before replacing the historical evidence.

## Router evaluation

`router_evaluation.json` is generated from the separate synthetic evaluation
CSV. It contains dataset hashes, confusion matrix, fallback reasons and failures.
The model card documents scope and reproduction. Synthetic routing accuracy is
not LLM answer quality.
