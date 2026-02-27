# Appendix E — Stakeholders + RACI (Governance)

## Stakeholders (minimum 6)
- Executive leadership
- IT Operations / SRE
- Data/AI team
- Cybersecurity & Compliance
- Procurement/Finance (FinOps/GreenOps)
- Cloud provider
- Grid / energy ecosystem actors
- Communities & partner agencies

## RACI (example)
| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Define carbon budget (gCO₂e/1k req) | Sustainability/FinOps | Exec sponsor | AI team, Ops | All teams |
| Routing policy (small-first thresholds) | AI team | AI lead | Ops, Security | Product |
| Cache policy (TTL/invalidations) | AI team | Ops lead | Security | Product |
| Logging & retention policy | Ops/Security | Security lead | AI team | Exec |
| Incident exceptions (heatwave mode) | Ops | Exec sponsor | AI+Security | Stakeholders |
| KPI reporting cadence | Sustainability | Exec sponsor | Ops/AI/Finance | All teams |
