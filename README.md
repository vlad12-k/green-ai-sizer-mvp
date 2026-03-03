[![Carbon Budget Gate](https://github.com/vlad12-k/green-ai-sizer-mvp/actions/workflows/carbon-budget.yml/badge.svg)](https://github.com/vlad12-k/green-ai-sizer-mvp/actions/workflows/carbon-budget.yml)

# Green AI Sizer MVP

Governance-first toolkit and evidence pack for **Responsible AI Sizing** (approved topic: reducing footprint via smaller models, caching, and inference control).  
This repository operationalises a practical governance question:

> **How do we prevent AI usage from silently increasing operational emissions while maintaining service readiness under heatwaves and grid volatility?**

It provides a reproducible method to **estimate and enforce CO₂e intensity per 1,000 AI requests** and documents boundary, assumptions, KPIs, stakeholders, and risks to support auditable decision-making.

---

## Table of contents
- [Context and problem statement](#context-and-problem-statement)
- [What is shipped in this repository](#what-is-shipped-in-this-repository)
- [Governance model](#governance-model)
- [Quickstart](#quickstart)
- [Carbon Budget Gate: how it works](#carbon-budget-gate-how-it-works)
- [Evidence pack](#evidence-pack)
- [Assumptions, boundary, and limitations](#assumptions-boundary-and-limitations)
- [Security and compliance posture](#security-and-compliance-posture)
- [Configuration](#configuration)
- [Verification checklist](#verification-checklist)
- [Roadmap (next hardening steps)](#roadmap-next-hardening-steps)
- [Product files](#product-files)
- [Versioning](#versioning)
- [License](#license)

---

## Context and problem statement
Climate-critical services increasingly rely on always-on digital systems (monitoring, reporting, coordination). Under **heatwaves**, cooling demand rises and infrastructure stress increases; under **grid volatility**, carbon intensity fluctuates and peak-demand constraints tighten.

AI-enabled workflows can improve responsiveness, but **uncontrolled inference demand** can become a baseline load (“always-on”), increasing emissions and cost unless governed through:
- **sizing** (small-first, big-if-needed),
- **caching** (avoid repeated compute),
- **inference control** (budgets, routing, policy thresholds).

This repository focuses on the **governance layer** first: measurable KPIs + enforceable CI gate + traceable evidence.

---

## What is shipped in this repository

### 1) CI governance: Carbon Budget Gate (required check)
- GitHub Actions workflow computes **gCO₂e / 1,000 requests** from workbook inputs.
- CI fails when the **improved** scenario exceeds the budget threshold.
- Results are surfaced in the GitHub Actions **run summary** (budget, baseline, improved, reduction).

### 2) Reproducible calculation method (workbook + calculator)
- Workbook: `workbook/appendix-d-baseline-improved.csv`
- Calculator: `workbook/calc_co2e.py`
- Outputs:
  - gCO₂e / 1k requests (baseline + improved)
  - total gCO₂e/day (baseline + improved)
  - estimated reduction vs baseline

### 3) Evidence pack (appendix-style documentation)
Designed for auditability and report insertion:
- Boundary & assumptions (Appendix C)
- Stakeholders & RACI (Appendix E)
- KPI definitions & reporting cadence (Appendix F)
- Risk register + mitigations (Appendix G)

### 4) Product-grade repository controls
- `main` is protected via ruleset:
  - PR-only merges
  - required checks (carbon-budget; CodeQL if enabled)
  - force-push blocked
- Code scanning (CodeQL) and dependency/security controls (where enabled)
- Reproducible development environment via Codespaces devcontainer

---

## Governance model
This repo treats sustainability as an enforceable constraint, not a narrative statement.

**Control points**
1. **Budget definition** (target gCO₂e/1k requests)
2. **Scenario inputs** (baseline vs improved)
3. **CI enforcement** (merge blocked if budget exceeded)
4. **Evidence trail** (run summary + versioned workbook + documented boundary)

**Why this matters**
Efficiency improvements alone can trigger **rebound effects** (lower cost → higher usage → higher total emissions). The gate is designed to support demand shaping and governance discipline rather than “optimize and hope”.

---

## Quickstart
This repo is a **governance-first evidence pack** for “Green AI sizing”: sustainability is treated as an enforceable constraint.  
You can reproduce the baseline vs improved scenario locally, verify evidence files, and (optionally) validate the live Azure Function endpoint.

### Run locally
```bash
python workbook/calc_co2e.py 200
```markdown
 What this does
	•	Reads scenario inputs from: workbook/appendix-d-baseline-improved.csv
	•	Uses grid intensity from: data/grid_intensity_uk_summary.json (and data/grid_intensity_uk_snapshot.csv)
	•	Computes:
	•	baseline gCO₂e per 1k requests
	•	improved gCO₂e per 1k requests
	•	total gCO₂e/day for the configured request volume
	•	Prints a PASS/FAIL decision against the given budget.

Expected output (shape)
	•	Baseline gCO₂e per 1k requests: …
	•	Improved gCO₂e per 1k requests: …
	•	PASS: Within budget. (or FAIL)

This same logic is enforced in CI by the Carbon Budget Gate workflow.



Reproducibility checklist (what a reviewer can verify)

Evidence artefacts in this repo:
	•	Workbook scenario inputs: workbook/appendix-d-baseline-improved.csv
	•	Calculator logic: workbook/calc_co2e.py
	•	Probe run evidence (endpoint metrics): scripts/probe_run_summary.json
	•	Probe script (how evidence was collected): scripts/probe_endpoint.py
	•	Real-world grid intensity snapshot: data/grid_intensity_uk_snapshot.csv + data/grid_intensity_uk_summary.json
	•	Data provenance note: docs/appendix-d-data-sources.md
	•	Security policy: SECURITY.md

---

### Live Azure endpoint (optional)

This MVP is deployed as an Azure Function (HTTP trigger) to demonstrate routing output (small vs large) and simulated per-request energy estimate (wh_request) under caching.

Security rules
	•	Never commit the function key (the ?code=... part).
	•	Store the full URL locally in a .env file (this repo ignores .env by design).

Example .env (local only):
URL='https://<your-function>.azurewebsites.net/api/orchestrator?code=<KEY>'

Minimal endpoint test (Codespaces / local)

set -a; source .env; set +a
curl -i -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{"query":"what is the heatwave incident checklist","seed":1}'

  Expected:
	•	HTTP/1.1 200 OK
	•	JSON containing: route, cache_hit, latency_ms, wh_request

---

Probe the endpoint (collect stable evidence)

This runs multiple requests and outputs aggregate metrics (cache hit rate, routing rate, latency percentiles, average Wh/request).

set -a; source .env; set +a
python scripts/probe_endpoint.py > scripts/probe_run_summary.json
cat scripts/probe_run_summary.json

Notes:
	•	The probe script reads URL from your environment (loaded from .env).
	•	The repo keeps the probe output under version control as evidence:
scripts/probe_run_summary.json

---

Budget-friendly operation (keep LIVE without burning credits)

Recommended practice:
	•	Do not run the probe repeatedly. Keep it to:
	•	once to generate evidence (already committed), and
	•	at most once per week if you intentionally refresh numbers.
	•	Keep “real data refresh” limited to grid intensity snapshots via GitHub Actions (no Azure runtime cost per request).
	•	If you want to pause Azure runtime costs, stop the Function App in Azure Portal and start it again when needed.
