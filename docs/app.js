'use strict';

const PATHS = {
  gridSummary: 'evidence/grid_intensity_uk_summary.json',
  probeSummary: 'evidence/probe_run_summary.json',
  workbookCSV: 'evidence/scenario-baseline-improved.csv'
};

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function fmt(n, d = 2) {
  return Number.isFinite(n) ? n.toFixed(d) : '—';
}

function pct(n) {
  return Number.isFinite(n) ? `${(n * 100).toFixed(1)} %` : '—';
}

function parseCSV(text) {
  const lines = text.trim().split('\n').filter(Boolean);
  if (lines.length < 2) return [];
  const headers = lines[0].split(',').map(x => x.trim());
  return lines.slice(1).map(line => {
    const vals = [];
    let cur = '';
    let inQ = false;
    for (const ch of line) {
      if (ch === '"') { inQ = !inQ; continue; }
      if (ch === ',' && !inQ) { vals.push(cur); cur = ''; continue; }
      cur += ch;
    }
    vals.push(cur);
    const row = {};
    headers.forEach((h, i) => { row[h] = (vals[i] || '').trim(); });
    return row;
  });
}

function calcRow(row) {
  const rpd = Number(row.requests_per_day);
  const cacheHit = Number(row.cache_hit_rate);
  const smallRate = Number(row.small_route_rate);
  const whSmall = Number(row.wh_small);
  const whLarge = Number(row.wh_large);
  const ci = Number(row.grid_intensity_g_per_kwh);
  if (![rpd, cacheHit, smallRate, whSmall, whLarge, ci].every(Number.isFinite) || rpd <= 0) {
    throw new Error('Malformed scenario row');
  }
  const computed = rpd * (1 - cacheHit);
  const small = computed * smallRate;
  const large = computed * (1 - smallRate);
  const whTotal = small * whSmall + large * whLarge;
  const kwhTotal = whTotal / 1000;
  const gco2Total = kwhTotal * ci;
  return gco2Total / (rpd / 1000);
}

async function fetchJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Missing or inaccessible file: ${path} (HTTP ${res.status})`);
  return res.json();
}

async function fetchText(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Missing or inaccessible file: ${path} (HTTP ${res.status})`);
  return res.text();
}

function updateState(kind, text) {
  const el = document.getElementById('dashboard-state');
  if (!el) return;
  el.className = `state-chip ${kind}`;
  el.textContent = text;
}

function getCommitHash() {
  const p = new URLSearchParams(window.location.search);
  const fromSha = p.get('sha');
  if (fromSha) return fromSha;
  const fromCommit = p.get('commit');
  if (fromCommit) return fromCommit;
  return null;
}

function renderProvenance(files) {
  const holder = document.getElementById('provenance-list');
  if (!holder) return;
  holder.innerHTML = '';
  const sha = getCommitHash();
  files.forEach(file => {
    const div = document.createElement('div');
    div.className = 'provenance-item';

    const rowFile = document.createElement('div');
    const fileStrong = document.createElement('strong');
    fileStrong.textContent = 'File:';
    const fileCode = document.createElement('code');
    fileCode.textContent = file;
    rowFile.appendChild(fileStrong);
    rowFile.appendChild(document.createTextNode(' '));
    rowFile.appendChild(fileCode);

    const rowCommit = document.createElement('div');
    const commitStrong = document.createElement('strong');
    commitStrong.textContent = 'Commit:';
    rowCommit.appendChild(commitStrong);
    rowCommit.appendChild(document.createTextNode(' '));
    if (sha) {
      const commitCode = document.createElement('code');
      commitCode.textContent = sha;
      rowCommit.appendChild(commitCode);
    } else {
      rowCommit.appendChild(document.createTextNode('Not available in page context'));
    }

    div.appendChild(rowFile);
    div.appendChild(rowCommit);
    holder.appendChild(div);
  });
}

function setupTooltips() {
  const tooltip = document.getElementById('tooltip');
  if (!tooltip) return;
  document.querySelectorAll('.tooltip-btn').forEach(btn => {
    const show = (e) => {
      tooltip.innerHTML = `${btn.dataset.tooltip} <a href="evidence/index.md" style="color:#9ce7bf">Evidence index</a>.`;
      tooltip.hidden = false;
      const x = e.clientX + 12;
      const y = e.clientY + 12;
      tooltip.style.left = `${x}px`;
      tooltip.style.top = `${y}px`;
    };
    const hide = () => { tooltip.hidden = true; };
    btn.addEventListener('mouseenter', show);
    btn.addEventListener('mousemove', show);
    btn.addEventListener('mouseleave', hide);
    btn.addEventListener('focus', () => {
      tooltip.innerHTML = `${btn.dataset.tooltip} <a href="evidence/index.md" style="color:#9ce7bf">Evidence index</a>.`;
      tooltip.hidden = false;
      const rect = btn.getBoundingClientRect();
      tooltip.style.left = `${rect.left + 12}px`;
      tooltip.style.top = `${rect.bottom + 8}px`;
    });
    btn.addEventListener('blur', hide);
  });
}

async function loadDashboard() {
  updateState('state-loading', 'Loading evidence…');

  const files = [PATHS.gridSummary, PATHS.probeSummary, PATHS.workbookCSV];
  renderProvenance(files);

  let grid, probe, csvText;
  try {
    [grid, probe, csvText] = await Promise.all([
      fetchJSON(PATHS.gridSummary),
      fetchJSON(PATHS.probeSummary),
      fetchText(PATHS.workbookCSV)
    ]);
  } catch (err) {
    updateState('state-error', 'Evidence file missing');
    setText('last-updated-text', `Error: ${err.message}`);
    return;
  }

  try {
    if (!grid || typeof grid !== 'object') throw new Error('Grid summary malformed');
    if (!probe || typeof probe !== 'object') throw new Error('Probe summary malformed');

    const rows = parseCSV(csvText);
    const baseline = rows.find(r => (r.scenario || '').toLowerCase() === 'baseline');
    const improved = rows.find(r => (r.scenario || '').toLowerCase() === 'improved');
    if (!baseline || !improved) throw new Error('Scenario CSV missing baseline/improved rows');

    const baselineG = calcRow(baseline);
    const improvedG = calcRow(improved);
    const reduction = baselineG > 0 ? ((1 - improvedG / baselineG) * 100) : NaN;

    setText('val-baseline', `${fmt(baselineG, 2)} g`);
    setText('val-improved', `${fmt(improvedG, 2)} g`);
    setText('val-reduction', `${fmt(reduction, 1)} %`);

    setText('val-cache', pct(Number(probe.cache_hit_rate_observed)));
    setText('val-route', pct(Number(probe.small_route_rate_observed)));

    const p95 = Number(probe.p95_latency_ms);
    setText('val-latency-p95', Number.isFinite(p95) ? `${fmt(p95, 0)} ms` : 'N/A');

    setText('val-grid-min', `${fmt(Number(grid.min_g_per_kwh), 1)} gCO₂/kWh`);
    setText('val-grid-avg', `${fmt(Number(grid.avg_g_per_kwh), 1)} gCO₂/kWh`);
    setText('val-grid-max', `${fmt(Number(grid.max_g_per_kwh), 1)} gCO₂/kWh`);

    if (grid.generated_utc) {
      setText('last-updated-text', `Last updated: ${new Date(grid.generated_utc).toUTCString()} (from evidence/grid_intensity_uk_summary.json)`);
    } else {
      setText('last-updated-text', 'Last updated: unavailable in summary JSON');
    }

    const hasPartial = !Number.isFinite(p95);
    updateState(hasPartial ? 'state-warn' : 'state-ok', hasPartial ? 'Loaded with partial metrics' : 'Loaded');
  } catch (err) {
    updateState('state-error', 'Malformed evidence data');
    setText('last-updated-text', `Error: ${err.message}`);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  setupTooltips();
  loadDashboard();
});
