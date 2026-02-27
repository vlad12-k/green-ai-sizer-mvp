# Appendix C — Assumptions & System Boundary

## System boundary (what is included)
This footprint method covers operational emissions for:
- Inference orchestration (routing + fallback logic)
- Caching (responses/semantic cache)
- Logging/metrics needed to compute KPIs
- Network overhead (simplified as a small factor if required)

## Exclusions (what is NOT included)
- End-user device energy use
- Embodied emissions of hardware (manufacture/disposal)
- Full data centre PUE modelling (treated as out of scope for MVP)

## Core assumptions (to be refined with Azure evidence)
- Requests per day: TBD (from Azure test run)
- Cache hit rate: TBD
- Small vs large routing rate: TBD
- Carbon intensity (gCO₂/kWh): from NESO/UK Carbon Intensity API (min/avg/max for sensitivity)
