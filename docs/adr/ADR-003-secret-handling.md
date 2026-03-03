# ADR-003 — Optional live endpoint and secret handling

**Status:** Accepted  
**Date:** 2026-03-01  
**Deciders:** AI team, Security lead

---

## Context

The Azure Function endpoint requires an authentication key (`?code=...`) that must never be committed to the repository. The team needed a safe local development pattern and clear guidance to prevent accidental key exposure, while still allowing the endpoint to be demonstrated and probed.

## Decision

- Store the full Function URL (including `?code=...`) in a local `.env` file only.
- The repository `.gitignore` explicitly excludes `.env` and `.env.*` (except `.env.example`).
- Documentation provides a safe example with a `<PLACEHOLDER>` key; no real key is ever shown.
- The probe script (`scripts/probe_endpoint.py`) reads `URL` from the environment, not from a hardcoded string.
- If a key is accidentally exposed, the SECURITY.md rotation procedure must be followed immediately.

## Rationale

- Prevents secret sprawl; keys exist only on the developer's machine or in GitHub Secrets.
- Pattern is standard (dotenv) and familiar; requires no additional tooling.
- `.env.example` can document the expected shape of the file without exposing real values.

## Consequences

- Developers must create their own `.env` before running the probe script.
- CI pipelines do not have access to the Function key; probe evidence is committed manually.
- Key rotation invalidates all existing `.env` copies held by developers.

## Alternatives considered

- **Hardcode key in CI secret and probe in CI:** rejected — would increase Azure call volume and cost; probe evidence should be intentional, not automatic.
- **OAuth / managed identity for local dev:** deferred — appropriate for production hardening but adds complexity at MVP stage.
