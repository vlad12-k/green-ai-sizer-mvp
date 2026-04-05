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

function renderProvenance(files, statuses) {
  const holder = document.getElementById('provenance-list');
  if (!holder) return;
  holder.innerHTML = '';
  files.forEach(file => {
    const div = document.createElement('div');
    div.className = 'provenance-item';
    const fileLine = document.createElement('div');
    fileLine.innerHTML = `<strong>File:</strong> <code>${file}</code>`;
    const status = statuses[file];
    const statusLine = document.createElement('div');
    statusLine.innerHTML = `<strong>Status:</strong> <span class="${status.ok ? 'status-ok' : 'status-fail'}">${status.ok ? 'loaded' : 'failed'}</span>${status.message ? ` — ${status.message}` : ''}`;
    div.appendChild(fileLine);
    div.appendChild(statusLine);
    holder.appendChild(div);
  });
}

function setupTabs() {
  const buttons = Array.from(document.querySelectorAll('.tab-btn'));
  const panels = {
    kpi: document.getElementById('tab-kpi'),
    charts: document.getElementById('tab-charts'),
    governance: document.getElementById('tab-governance'),
    provenance: document.getElementById('tab-provenance')
  };
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      document.body.dataset.activeTab = target;
      buttons.forEach(b => {
        const selected = b === btn;
        b.classList.toggle('active', selected);
        b.setAttribute('aria-selected', selected ? 'true' : 'false');
      });
      Object.entries(panels).forEach(([name, panel]) => {
        const active = name === target;
        if (panel) {
          panel.classList.toggle('active', active);
          panel.hidden = !active;
          panel.setAttribute('aria-hidden', active ? 'false' : 'true');
        }
      });
    });
  });
}

function setLastUpdated(grid) {
  if (grid && grid.generated_utc) {
    setText('last-updated-text', `Last updated: ${new Date(grid.generated_utc).toUTCString()} (from docs/evidence/grid_intensity_uk_summary.json)`);
  } else {
    setText('last-updated-text', 'Last updated: unavailable in summary JSON');
  }
}

function renderBarChart(svgId, labels, values, suffix = '') {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  svg.innerHTML = '';
  const width = 360;
  const height = 180;
  const margin = { top: 10, right: 10, bottom: 28, left: 28 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const max = Math.max(...values.filter(Number.isFinite), 1);

  labels.forEach((label, i) => {
    const value = Number(values[i]);
    const barW = innerW / labels.length - 12;
    const x = margin.left + i * (barW + 12);
    const barH = Number.isFinite(value) ? (value / max) * innerH : 0;
    const y = margin.top + (innerH - barH);

    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', String(x));
    rect.setAttribute('y', String(y));
    rect.setAttribute('width', String(barW));
    rect.setAttribute('height', String(barH));
    rect.setAttribute('fill', i === 1 ? '#1d8a55' : '#7dbf9f');
    if (i === 1) rect.setAttribute('stroke', '#0b5633');
    if (i === 1) rect.setAttribute('stroke-width', '2');
    svg.appendChild(rect);

    const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
    title.textContent = `${label}: ${Number.isFinite(value) ? `${fmt(value, 1)}${suffix}` : 'unavailable'}`;
    rect.appendChild(title);

    const txt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    txt.setAttribute('x', String(x + (barW / 2)));
    txt.setAttribute('y', String(y - 4));
    txt.setAttribute('text-anchor', 'middle');
    txt.setAttribute('font-size', '11');
    txt.textContent = Number.isFinite(value) ? `${fmt(value, 1)}${suffix}` : '—';
    svg.appendChild(txt);

    const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    lbl.setAttribute('x', String(x + (barW / 2)));
    lbl.setAttribute('y', String(height - 8));
    lbl.setAttribute('text-anchor', 'middle');
    lbl.setAttribute('font-size', '11');
    lbl.textContent = label;
    svg.appendChild(lbl);
  });
}

async function loadDashboard() {
  updateState('state-loading', 'Loading evidence…');
  setupTabs();
  document.body.dataset.activeTab = 'kpi';

  const files = [PATHS.gridSummary, PATHS.probeSummary, PATHS.workbookCSV];
  const statuses = {};
  files.forEach(f => { statuses[f] = { ok: false, message: 'not loaded' }; });

  let grid, probe, csvText;
  try {
    grid = await fetchJSON(PATHS.gridSummary);
    statuses[PATHS.gridSummary] = { ok: true, message: '' };
  } catch (err) {
    statuses[PATHS.gridSummary] = { ok: false, message: err.message };
  }
  try {
    probe = await fetchJSON(PATHS.probeSummary);
    statuses[PATHS.probeSummary] = { ok: true, message: '' };
  } catch (err) {
    statuses[PATHS.probeSummary] = { ok: false, message: err.message };
  }
  try {
    csvText = await fetchText(PATHS.workbookCSV);
    statuses[PATHS.workbookCSV] = { ok: true, message: '' };
  } catch (err) {
    statuses[PATHS.workbookCSV] = { ok: false, message: err.message };
  }

  renderProvenance(files, statuses);

  if (!statuses[PATHS.gridSummary].ok || !statuses[PATHS.probeSummary].ok || !statuses[PATHS.workbookCSV].ok) {
    updateState('state-error', 'Evidence file missing');
    setText('last-updated-text', 'Last updated: unavailable (one or more files failed to load)');
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
    const avgLatency = Number(probe.avg_latency_ms);
    setText('val-latency-avg', Number.isFinite(avgLatency) ? `${fmt(avgLatency, 0)} ms` : 'N/A');

    const p95 = Number(probe.p95_latency_ms);
    setText('val-latency-p95', Number.isFinite(p95) ? `${fmt(p95, 0)} ms` : 'N/A');

    const gridMin = Number(grid.min_g_per_kwh);
    const gridAvg = Number(grid.avg_g_per_kwh);
    const gridMax = Number(grid.max_g_per_kwh);
    setText('val-grid-min', `${fmt(gridMin, 1)} gCO₂/kWh`);
    setText('val-grid-avg', `${fmt(gridAvg, 1)} gCO₂/kWh`);
    setText('val-grid-max', `${fmt(gridMax, 1)} gCO₂/kWh`);
    setLastUpdated(grid);

    renderBarChart('chart-carbon', ['Baseline', 'Improved'], [baselineG, improvedG], 'g');
    renderBarChart('chart-grid', ['Min', 'Avg', 'Max'], [gridMin, gridAvg, gridMax], '');

    const hasPartial = !Number.isFinite(p95);
    updateState(hasPartial ? 'state-warn' : 'state-ok', hasPartial ? 'Loaded with partial metrics' : 'Loaded');
  } catch (err) {
    updateState('state-error', 'Malformed evidence data');
    setText('last-updated-text', `Last updated: error (${err.message})`);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadDashboard();
});
