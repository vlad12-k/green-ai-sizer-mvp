# Privacy statement

## Data classification

This repository is a governance evidence pack. It contains no personal data, no clinical data, and no sensitive operational data.

## What this repository contains

| Data type | Description | Classification |
|---|---|---|
| UK grid carbon intensity | Public data from the NESO / UK Carbon Intensity API; aggregated min/avg/max readings | Public |
| Workbook scenario parameters | Synthetic engineering parameters (requests/day, routing rates, Wh estimates) | Internal / non-sensitive |
| Probe run summary | Aggregate performance metrics from a test endpoint (latency, cache hit rate, routing rate); no prompt content is recorded | Internal / non-sensitive |
| Route training labels | Synthetic prompt category labels used for routing model development | Internal / non-sensitive |
| Azure Function responses | Routed requests return route, cache hit flag, latency, and Wh estimate; no prompt text is stored in committed files | Internal / non-sensitive |

## What this repository does NOT contain

- Names, email addresses, or any personally identifiable information (PII).
- Clinical, health, or patient data.
- Financial or commercially sensitive data.
- Customer or end-user data of any kind.
- Real operational prompts or query content.

## Data handling principles

1. **Minimisation:** only the minimum data needed to evidence governance controls is collected and committed.
2. **Public sources only:** grid intensity data is sourced from a public, no-authentication API.
3. **Synthetic prompts:** all routing test prompts are synthetic and contain no real user input.
4. **No long-term retention of endpoint calls:** the probe script runs a bounded number of requests and discards individual responses; only aggregate metrics are committed.
5. **No logging of secrets or credentials:** function keys and environment variables must not appear in committed files, logs, or GitHub Actions summaries.

## Review

This statement should be reviewed if:

- A new data source is added that could contain personal or sensitive data.
- The probe script is modified to log prompt content.
- The system is extended to handle real user queries.

Owner: AI team / Compliance lead. Evidence: `docs/governance/controls.md` (C-05).
