# Security policy

This repository is a governance-first evidence pack. Security and data discipline are treated as first-class requirements.

---

## Secrets and credentials

Do not commit any of the following:

- Azure Function keys, access tokens, client secrets, or credentials.
- `.env` files containing secrets (this repository ignores `.env` by design; see `.gitignore`).
- Any URL containing `?code=...` or equivalent authentication parameters.
- Customer, clinical, or personally identifiable data.

Store the deployed Azure Function URL (including `?code=...`) locally in a `.env` file only.

---

## Key rotation (Azure Functions)

If a function key is accidentally exposed (committed to a repository, posted in an issue, or visible in a log), rotate it **immediately**:

1. Open **Azure Portal** → Function App → **Functions** → `orchestrator` → **Function Keys**.
2. Click the ellipsis next to the affected key → **Renew key value** (or **Regenerate**).
3. Copy the new key value.
4. Update your local `.env` file with the new URL.
5. If the key is stored in a GitHub Secret, update it under **Repository Settings** → **Secrets and variables** → **Actions**.
6. Confirm the old key is invalidated by testing with the old URL (expect HTTP 401).

Detailed steps are also in `docs/runbook.md` (section 2).

---

## Dependency and code scanning

- Keep GitHub Actions workflows enabled (Carbon Budget Gate, Azure deploy).
- Use **Dependabot** alerts for dependency vulnerability tracking.
- **CodeQL** is configured as a required check where enabled; do not disable it.
- Review and action alerts promptly, particularly any marked Critical or High.

---

## Branch protection

The `main` branch is protected:

- Direct commits are blocked; all changes require a pull request.
- Required checks must pass before merge (Carbon Budget Gate; CodeQL if enabled).
- Force-push is blocked.

---

## Data policy

This repository may include:

- Public grid carbon intensity snapshots from official public APIs (NESO / UK Carbon Intensity API).
- Synthetic prompts for routing tests; no real user input.

It must not include sensitive operational data, personal data, or clinical data. See `PRIVACY.md` for the full data classification statement.

---

## Reporting a vulnerability

If you identify a security issue in this repository, please open a GitHub issue with the label `security`. For sensitive disclosures, contact the repository owner directly rather than posting details publicly.
