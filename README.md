[![Carbon Budget Gate](https://github.com/vlad12-k/green-ai-sizer-mvp/actions/workflows/carbon-budget.yml/badge.svg)](https://github.com/vlad12-k/green-ai-sizer-mvp/actions/workflows/carbon-budget.yml)

# Green AI Sizer MVP

A governance-first toolkit and evidence pack for **Responsible AI Sizing** (approved topic: *reducing footprint through smaller models, caching, and inference control*).  
It provides a reproducible method to **estimate and govern CO₂e intensity per 1,000 AI requests** and to document the technical, governance, and risk assumptions required for **climate-critical digital services** operating under **heatwaves and grid volatility**.

This repository is intentionally built as a **reviewable product artefact**: assumptions are explicit, calculations are versioned, CI enforces a measurable target, and the evidence pack maps directly to the report sections and learning outcomes.

---

## Table of contents
- [Problem context](#problem-context)
- [What this repository delivers](#what-this-repository-delivers)
- [Product scope](#product-scope)
- [Quickstart](#quickstart)
- [How the Carbon Budget Gate works](#how-the-carbon-budget-gate-works)
- [Evidence and appendices](#evidence-and-appendices)
- [Alignment with learning outcomes](#alignment-with-learning-outcomes)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Verification checklist](#verification-checklist)
- [Roadmap](#roadmap)
- [Versioning](#versioning)
- [License](#license)

---

## Problem context

Climate-focused organisations increasingly depend on always-on digital services (monitoring, reporting, coordination). Under **heatwaves**, cooling demand rises and infrastructure stress increases; under **grid volatility**, carbon intensity and operational constraints fluctuate.  
AI-enabled services can improve responsiveness, but **uncontrolled inference demand** can become a baseline load (“always-on”), increasing emissions and cost unless it is governed through sizing, caching, and routing.

**Responsible AI Sizing** aims to:
- reduce unnecessary high-cost inference,
- prevent rebound effects (efficiency → more usage → higher total emissions),
- keep reliability and security acceptable during peak climate stress.

---

## What this repository delivers

### 1) Carbon Budget Gate (CI governance)
A GitHub Actions workflow computes **gCO₂e / 1,000 requests** from the workbook and fails CI if the threshold is exceeded.  
This provides an enforceable control to prevent silent footprint growth.

### 2) Carbon calculation workbook + calculator (reproducible LO4 evidence)
- `workbook/appendix-d-baseline-improved.csv` stores **baseline vs improved** scenarios.
- `workbook/calc_co2e.py` computes:
  - CO₂e intensity per 1,000 requests
  - total daily CO₂e
  - reduction estimate vs baseline
- Results are surfaced in the GitHub Actions run summary for traceability.

### 3) Evidence pack (Appendices C–G)
A structured set of appendices designed for Overleaf/QUB template insertion:
- system boundary and assumptions,
- stakeholder governance,
- KPI definitions,
- risk register with mitigation and burden-shifting logic.

---

## Product scope

### This repository provides
- A **measurable governance mechanism** (budget enforcement in CI).
- A **reproducible calculation method** (workbook + calculator).
- A **traceable evidence layer** aligned to the report requirements (appendices).

### This repository does not claim (by design)
- **Production-grade carbon accounting**: energy-per-request values are scenario inputs and must be validated with telemetry (planned Azure MVP).
- Full lifecycle accounting (embodied emissions, full PUE modelling, end-user devices) unless explicitly added to Appendix C.

This scope boundary is deliberate to keep the artefact auditable and aligned with the assignment’s system-boundary approach.

---

## Quickstart

### Run locally (or in Codespaces)
```bash
python workbook/calc_co2e.py 200
