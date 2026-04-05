# Operator runbook

This runbook covers the four primary operator tasks: validating the CI Carbon Budget Gate, rotating the Azure Function key, refreshing evidence data, and pausing Azure spend.

---

## 1. Validate the CI Carbon Budget Gate

**When to use:** after any change to workbook inputs or calculator logic; when verifying CI is passing.

**Local validation:**

```bash
python workbook/calc_co2e.py 200
```

Expected output (current values):

```
Budget (gCO2e/1k): 200.00
Baseline gCO2e per 1k requests: 159.70 gCO2e
Baseline total gCO2e/day: 159.70 gCO2e
Improved gCO2e per 1k requests: 50.69 gCO2e
Improved total gCO2e/day: 50.69 gCO2e
PASS: Within budget.
```

If you see `FAIL: Budget exceeded`, the improved scenario in `data/scenario-baseline-improved.csv` exceeds the budget. Either reduce the improved scenario metrics or raise the budget by updating the workflow call in `.github/workflows/carbon-budget.yml`.

**In CI (GitHub Actions):**

1. Navigate to **Actions** → **Carbon Budget Gate**.
2. Open the latest run for your branch.
3. Check the **Run CO2e budget check** step log and the **Step Summary** panel.
4. A green tick indicates PASS; a red cross indicates FAIL with the breach details.

**Evidence artefacts:** `data/scenario-baseline-improved.csv`, `workbook/calc_co2e.py`, `.github/workflows/carbon-budget.yml`

---

## 2. Rotate the Azure Function key

**When to use:** if a function key (`?code=...`) is accidentally exposed in a commit, log, or public channel; or on a scheduled rotation.

**Steps:**

1. Open **Azure Portal** → your Function App (`func-green-ai-sizer-mvp-01`).
2. Navigate to **Functions** → `orchestrator` → **Function Keys**.
3. Click the ellipsis next to the affected key → **Renew key value** (or **Regenerate**).
4. Copy the new key value.
5. Update your local `.env` file:
   ```
   URL='https://func-green-ai-sizer-mvp-01.azurewebsites.net/api/orchestrator?code=<NEW-KEY>'
   ```
6. If the key is stored in GitHub Secrets (e.g., for a CI probe), update the secret in **Repository Settings** → **Secrets and variables** → **Actions**.
7. Confirm the old key is invalidated by attempting a request with the old URL — it should return 401.

**Do not:** commit the new key value to any file; print it in logs; share it in issues or PR comments.

**Evidence artefact:** `SECURITY.md`

---

## 3. Refresh evidence data

### 3a. Grid intensity snapshot (automated)

The `refresh-grid-intensity.yml` workflow runs daily at 06:10 UTC and updates `data/grid_intensity_uk_snapshot.csv` and `data/grid_intensity_uk_summary.json` on the `dev` branch.

**To trigger manually:**

1. Navigate to **Actions** → **Refresh UK grid intensity snapshot**.
2. Click **Run workflow** → select branch `dev` → **Run workflow**.
3. After the workflow completes, verify the updated `generated_utc` in `data/grid_intensity_uk_summary.json`.

**To refresh locally:**

```bash
python scripts/fetch_uk_grid_intensity.py
```

This writes updated files to `data/`. Do not commit these locally unless you intend to update the evidence baseline.

### 3b. Probe run summary (manual)

The probe summary is updated deliberately, not automatically. Probe evidence should be refreshed when endpoint behaviour changes (routing thresholds, cache policy, scaling).

**Steps:**

```bash
# Ensure .env contains the current Function URL
set -a; source .env; set +a

# Run the probe and capture output
python scripts/probe_endpoint.py > scripts/probe_run_summary.json

# Review the output
cat scripts/probe_run_summary.json
```

If the new values are materially different, update `data/scenario-baseline-improved.csv` (improved scenario fields: `cache_hit_rate`, `small_route_rate`, `avg_latency_ms`, `p95_latency_ms`) and re-run the budget check.

**Frequency:** at most once per week; only when endpoint configuration has changed.

**Evidence artefact:** `scripts/probe_run_summary.json`, `docs/evidence/data-sources.md`

---

## 4. Pause Azure spend

**When to use:** when no active development requires the Function App to be running; to avoid idle compute charges.

**Steps to stop:**

1. Open **Azure Portal** → Function App `func-green-ai-sizer-mvp-01`.
2. Navigate to **Overview** → click **Stop**.
3. Confirm the app status changes to **Stopped**.

**Steps to restart:**

1. Open **Azure Portal** → Function App `func-green-ai-sizer-mvp-01`.
2. Navigate to **Overview** → click **Start**.
3. Wait for status to become **Running** (typically 30–60 seconds).
4. Validate: `curl -i -X POST "$URL" -H "Content-Type: application/json" -d '{"query":"test"}'` — expect HTTP 200.

**Notes:**

- Stopping the Function App does not affect CI, the dashboard, or the evidence files.
- Grid intensity refresh does not call the Function App; it will continue unaffected.
- The Azure deploy workflow (`.github/workflows/dev_func-green-ai-sizer-mvp-01.yml`) will restart the app on the next push to `main`.

---

## 5. Evidence audit checklist

Use this checklist during quarterly governance reviews:

- [ ] Run `python workbook/calc_co2e.py 200` locally — confirm PASS and current values.
- [ ] Verify `data/grid_intensity_uk_summary.json` has a `generated_utc` within the last 7 days (or trigger manual refresh).
- [ ] Confirm `scripts/probe_run_summary.json` reflects current endpoint configuration.
- [ ] Review `data/scenario-baseline-improved.csv` — confirm improved scenario fields match probe summary.
- [ ] Check `.gitignore` still excludes `.env` and `.env.*`.
- [ ] Review `docs/governance/risk-register.md` for any new or changed risks.
- [ ] Check `docs/governance/controls.md` review cadence dates are current.
- [ ] Confirm no secrets appear in recent commits: `git log --all --oneline | head -20` and review diffs for `?code=` patterns.
