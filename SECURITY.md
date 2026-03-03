# Security policy

This repository is a governance-first evidence pack. Security and data discipline are treated as first-class requirements.

## Secrets and credentials
Do not commit any of the following:
- Azure Function keys, access tokens, client secrets, credentials
- `.env` files containing secrets (this repo ignores `.env` by design)
- customer / clinical / personal data

Store the deployed Azure Function URL (including `?code=...`) locally in a `.env` file.

## Key rotation (Azure Functions)
If a function key is exposed, rotate it immediately:
Azure Portal → Function App → Functions → `orchestrator` → Function Keys → regenerate the affected key.

After rotation, update your local `.env`.

## Dependency and code scanning
- Keep GitHub Actions workflows enabled.
- Use Dependabot alerts and CodeQL (if enabled) for continuous scanning.

## Data policy
This repository may include:
- public grid carbon intensity snapshots from official/public APIs
- synthetic prompts for routing tests

It must not include sensitive operational or personal data. 
