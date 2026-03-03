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

### Run locally
```bash
python workbook/calc_co2e.py 200

