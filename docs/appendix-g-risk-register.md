# Appendix G — Risk Register

| Risk | Cause | Impact | Likelihood | Mitigation | Burden shifting (where impact moves) |
|---|---|---|---|---|---|
| Rebound effect | AI becomes cheaper/faster → more use | Total CO₂e rises | Medium | Budgets, quotas, feature-level accounting | More policy work / user friction |
| Quality degradation | Overuse of “small” path | Wrong decisions | Medium | Confidence thresholds + fallback + eval | More “large” calls in edge cases |
| Privacy / sensitive data | Logging prompts/responses | Compliance breach | Medium | Minimise logs, redact, retention limits | Less debug detail |
| Vendor lock-in | Azure-specific services | Hard to migrate | Low–Med | Keep interfaces abstract, document mapping | More engineering upfront |
| Heatwave outage | Grid/cooling stress | Service downtime | Medium | Graceful degradation, cache-first mode | Reduced response richness |
| Monitoring overhead | Excess logging/metrics | Higher storage/CO₂e | Medium | Sampling, retention policies | Less observability |
