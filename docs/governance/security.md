# Governance Security

This document defines governance-level security controls and references implementation policy.

## Security controls
- Secrets are never committed to source control.
- `.env` and `.env.*` are excluded from version control.
- CI checks must remain enabled for budget and code scanning coverage.
- Security incidents require immediate key rotation and evidence update.

## Security runbook references
- Policy: `SECURITY.md`
- Operator process: `docs/governance/runbook.md`
- Controls mapping: `docs/governance/controls.md`
- Threat analysis: `THREAT_MODEL.md`

## Review cadence
- Review quarterly during governance review.
- Review immediately after any security incident or key exposure.
