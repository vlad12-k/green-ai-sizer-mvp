# Appendix F — KPI Set (Definitions)

## Core KPIs
- **gCO₂e / 1,000 requests**
  - Derived from: kWh estimate × grid carbon intensity (gCO₂/kWh)
- **Cache hit rate (%)**
  - cache_hits / total_requests
- **% small model routing**
  - small_routed / (small_routed + large_routed)
- **p95 latency (ms)**
  - 95th percentile response time from test logs
- **Monthly CO₂e trend**
  - from workbook using measured traffic + CI scenarios
- **AI call rate per feature/team**
  - requests grouped by `feature` tag (used to detect rebound)

## Reporting cadence (recommended)
- Weekly: cache hit, routing %, p95 latency
- Monthly: gCO₂e/1k, total estimated CO₂e, top features by AI demand
- Quarterly: governance review (budgets, exceptions, risks)
