/**
 * Green AI Sizer MVP — Dashboard application logic
 * Static GitHub Pages. No external libraries. No external API calls.
 *
 * Evidence sources (all values come from these files only):
 *   - ../workbook/appendix-d-baseline-improved.csv
 *   - ../data/grid_intensity_uk_summary.json
 *   - ../scripts/probe_run_summary.json
 */

'use strict';

/* ============================================================
   Tab navigation
   ============================================================ */
function initTabs() {
  const buttons = document.querySelectorAll('.tab-btn');
  const panels  = document.querySelectorAll('.tab-panel');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      buttons.forEach(b => {
        b.classList.toggle('active', b.dataset.tab === target);
        b.setAttribute('aria-selected', b.dataset.tab === target ? 'true' : 'false');
      });
      panels.forEach(p => {
        const match = p.id === 'panel-' + target;
        p.classList.toggle('active', match);
        p.hidden = !match;
      });
    });

    btn.addEventListener('keydown', e => {
      const idx  = Array.from(buttons).indexOf(e.currentTarget);
      if (e.key === 'ArrowRight') buttons[(idx + 1) % buttons.length].focus();
      if (e.key === 'ArrowLeft')  buttons[(idx - 1 + buttons.length) % buttons.length].focus();
    });
  });
}

/* ============================================================
   Helpers
   ============================================================ */
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function setClass(id, cls) {
  const el = document.getElementById(id);
  if (el) el.classList.add(cls);
}

function fmt(n, decimals) {
  if (n === null || n === undefined || isNaN(n)) return '—';
  return Number(n).toFixed(decimals !== undefined ? decimals : 2);
}

function pct(n) {
  return fmt(n * 100, 1) + ' %';
}

/* Parse a minimal CSV string into an array of objects */
function parseCSV(text) {
  const lines = text.trim().split('\n').filter(l => l.trim() !== '');
  if (lines.length < 2) return [];
  const headers = lines[0].split(',').map(h => h.trim());
  return lines.slice(1).map(line => {
    /* handle quoted fields with commas */
    const fields = [];
    let cur = '', inQ = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') { inQ = !inQ; continue; }
      if (ch === ',' && !inQ) { fields.push(cur.trim()); cur = ''; continue; }
      cur += ch;
    }
    fields.push(cur.trim());
    const obj = {};
    headers.forEach((h, i) => { obj[h] = fields[i] !== undefined ? fields[i] : ''; });
    return obj;
  });
}

/* ============================================================
   Fetch evidence files relative to this script's location
   ============================================================ */
async function fetchJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error('HTTP ' + res.status + ' fetching ' + path);
  const lastMod = res.headers.get('Last-Modified') || null;
  const data = await res.json();
  return { data, lastMod };
}

async function fetchText(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error('HTTP ' + res.status + ' fetching ' + path);
  const lastMod = res.headers.get('Last-Modified') || null;
  const text = await res.text();
  return { text, lastMod };
}

/* ============================================================
   CO₂e calculations (mirroring workbook/calc_co2e.py)
   ============================================================ */
function calcRow(row) {
  const rpd       = parseFloat(row.requests_per_day);
  const cacheHit  = parseFloat(row.cache_hit_rate);
  const smallRate = parseFloat(row.small_route_rate);
  const whSmall   = parseFloat(row.wh_small);
  const whLarge   = parseFloat(row.wh_large);
  const ci        = parseFloat(row.grid_intensity_g_per_kwh);

  const computed = rpd * (1.0 - cacheHit);
  const small    = computed * smallRate;
  const large    = computed * (1.0 - smallRate);
  const whTotal  = small * whSmall + large * whLarge;
  const kwhTotal = whTotal / 1000.0;
  const gco2Total = kwhTotal * ci;
  const gPer1k   = gco2Total / (rpd / 1000.0);
  return { gPer1k, gco2Total };
}

/* ============================================================
   SVG chart helpers
   ============================================================ */
function svgEl(tag, attrs) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
}

/**
 * Draw a simple horizontal bar chart into an <svg> element.
 * bars: [{ label, value, color }]
 * maxVal: scale maximum
 */
function drawBarChart(svgId, bars, maxVal, unit) {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  svg.innerHTML = '';

  const W      = svg.parentElement.clientWidth || 400;
  const barH   = 34;
  const gapY   = 14;
  const padL   = 160;  /* label area */
  const padR   = 60;   /* value label */
  const padT   = 16;
  const chartW = Math.max(W - padL - padR, 80);
  const totalH = padT + bars.length * (barH + gapY) + 24;

  svg.setAttribute('height', totalH);
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + totalH);

  const scale = v => (v / maxVal) * chartW;

  bars.forEach((bar, i) => {
    const y = padT + i * (barH + gapY);

    /* label */
    const lbl = svgEl('text', {
      x: padL - 10, y: y + barH / 2 + 4,
      'text-anchor': 'end', class: 'bar-label'
    });
    lbl.textContent = bar.label;
    svg.appendChild(lbl);

    /* bar */
    const rect = svgEl('rect', {
      x: padL, y: y,
      width: Math.max(scale(bar.value), 2),
      height: barH,
      rx: 4,
      fill: bar.color || '#2e9e5e'
    });
    svg.appendChild(rect);

    /* value label */
    const val = svgEl('text', {
      x: padL + scale(bar.value) + 6,
      y: y + barH / 2 + 4,
      class: 'bar-value'
    });
    val.textContent = fmt(bar.value, 1) + (unit ? ' ' + unit : '');
    svg.appendChild(val);
  });

  /* axis line */
  const axis = svgEl('line', {
    x1: padL, y1: padT - 4,
    x2: padL, y2: totalH - 20,
    stroke: '#d1d9e0', 'stroke-width': 1
  });
  svg.appendChild(axis);
}

/* ============================================================
   Main data load & render
   ============================================================ */
const BUDGET = 200.0;

/* Relative paths from docs/ to data files */
const PATHS = {
  gridSummary:  '../data/grid_intensity_uk_summary.json',
  probeSummary: '../scripts/probe_run_summary.json',
  workbookCSV:  '../workbook/appendix-d-baseline-improved.csv'
};

async function loadAndRender() {
  const lastUpdatedEl = document.getElementById('last-updated-text');
  const provenanceEl  = document.getElementById('provenance-list');

  let gridData   = null, gridLastMod   = null;
  let probeData  = null, probeLastMod  = null;
  let csvRows    = null, csvLastMod    = null;

  const provenance = [];

  /* --- Load grid intensity --------------------------------- */
  try {
    const r = await fetchJSON(PATHS.gridSummary);
    gridData   = r.data;
    gridLastMod = r.lastMod;
    provenance.push({
      file: 'data/grid_intensity_uk_summary.json',
      desc: 'UK grid carbon intensity — min/avg/max (last 24 h, half-hourly)',
      lastMod: gridLastMod || (gridData.generated_utc ? gridData.generated_utc : null),
      status: 'ok',
      statusLabel: 'Loaded'
    });
  } catch (e) {
    provenance.push({ file: 'data/grid_intensity_uk_summary.json', desc: 'Grid intensity summary', lastMod: null, status: 'err', statusLabel: 'Failed to load: ' + e.message });
  }

  /* --- Load probe summary ---------------------------------- */
  try {
    const r = await fetchJSON(PATHS.probeSummary);
    probeData   = r.data;
    probeLastMod = r.lastMod;
    provenance.push({
      file: 'scripts/probe_run_summary.json',
      desc: 'Endpoint probe run — cache hit rate, routing, latency, Wh/request',
      lastMod: probeLastMod,
      status: 'ok',
      statusLabel: 'Loaded'
    });
  } catch (e) {
    provenance.push({ file: 'scripts/probe_run_summary.json', desc: 'Probe run summary', lastMod: null, status: 'err', statusLabel: 'Failed to load: ' + e.message });
  }

  /* --- Load workbook CSV ----------------------------------- */
  try {
    const r = await fetchText(PATHS.workbookCSV);
    csvRows   = parseCSV(r.text);
    csvLastMod = r.lastMod;
    provenance.push({
      file: 'workbook/appendix-d-baseline-improved.csv',
      desc: 'Workbook scenario inputs — baseline vs improved',
      lastMod: csvLastMod,
      status: 'ok',
      statusLabel: 'Loaded'
    });
  } catch (e) {
    provenance.push({ file: 'workbook/appendix-d-baseline-improved.csv', desc: 'Workbook CSV', lastMod: null, status: 'err', statusLabel: 'Failed to load: ' + e.message });
  }

  /* ========================================================
     KPI population
     ======================================================== */

  /* Grid intensity */
  if (gridData) {
    setText('val-grid-avg',   fmt(gridData.avg_g_per_kwh, 2) + ' gCO₂/kWh');
    setText('val-grid-range',
      fmt(gridData.min_g_per_kwh, 1) + ' – ' + fmt(gridData.max_g_per_kwh, 1) + ' gCO₂/kWh');
  }

  /* Probe metrics */
  if (probeData) {
    setText('val-cache',        pct(probeData.cache_hit_rate_observed));
    setText('val-route',        pct(probeData.small_route_rate_observed));
    setText('val-latency-avg',  fmt(probeData.avg_latency_ms, 0) + ' ms');
    setText('val-latency-p95',  fmt(probeData.p95_latency_ms, 0) + ' ms');
    setText('val-wh',           fmt(probeData.avg_wh_request, 4) + ' Wh');
  }

  /* Workbook / CO₂e */
  if (csvRows && csvRows.length > 0) {
    const baselineRow  = csvRows.find(r => r.scenario && r.scenario.trim().toLowerCase() === 'baseline');
    const improvedRow  = csvRows.find(r => r.scenario && r.scenario.trim().toLowerCase() === 'improved');

    let baselineG = null, improvedG = null;

    if (baselineRow) {
      try {
        const res = calcRow(baselineRow);
        baselineG = res.gPer1k;
        setText('val-baseline', fmt(baselineG, 2) + ' g');
      } catch (_) { setText('val-baseline', 'Calc error'); }
    }

    if (improvedRow) {
      try {
        const res = calcRow(improvedRow);
        improvedG = res.gPer1k;
        setText('val-improved', fmt(improvedG, 2) + ' g');

        const pass = improvedG <= BUDGET;
        setText('val-budget-status', pass ? 'PASS' : 'FAIL');
        setClass('val-budget-status', pass ? 'pass' : 'fail');
      } catch (_) { setText('val-improved', 'Calc error'); }
    }

    if (baselineG !== null && improvedG !== null && baselineG > 0) {
      const reduction = (1.0 - improvedG / baselineG) * 100.0;
      setText('val-reduction', fmt(reduction, 1) + ' %');
    }
  }

  /* Last updated */
  const gridTs = gridData && gridData.generated_utc ? gridData.generated_utc : null;
  if (gridTs) {
    lastUpdatedEl.textContent =
      'Grid intensity last refreshed: ' + new Date(gridTs).toUTCString() +
      ' · Data sourced from data/grid_intensity_uk_summary.json (NESO UK Carbon Intensity API)';
  } else {
    lastUpdatedEl.textContent = 'Last updated: page loaded at ' + new Date().toUTCString();
  }

  /* ========================================================
     Charts
     ======================================================== */

  /* CO₂e bar chart */
  if (csvRows) {
    const baselineRow = csvRows.find(r => r.scenario && r.scenario.trim().toLowerCase() === 'baseline');
    const improvedRow = csvRows.find(r => r.scenario && r.scenario.trim().toLowerCase() === 'improved');
    const bars = [];
    if (baselineRow) {
      try { bars.push({ label: 'Baseline', value: calcRow(baselineRow).gPer1k, color: '#8ab8a4' }); } catch (_) {}
    }
    if (improvedRow) {
      try { bars.push({ label: 'Improved', value: calcRow(improvedRow).gPer1k, color: '#1a6e3e' }); } catch (_) {}
    }
    /* Budget marker as a pseudo-bar at the budget line */
    if (bars.length > 0) {
      const maxVal = Math.max(BUDGET * 1.1, ...bars.map(b => b.value));
      drawBarChart('svg-co2e', bars, maxVal, 'gCO₂e/1k');

      /* Add budget line annotation */
      const svgEl2 = document.getElementById('svg-co2e');
      if (svgEl2) {
        const W      = svgEl2.parentElement.clientWidth || 400;
        const padL   = 160;
        const padR   = 60;
        const chartW = Math.max(W - padL - padR, 80);
        const x      = padL + (BUDGET / maxVal) * chartW;
        const h      = parseInt(svgEl2.getAttribute('height') || 240, 10);

        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x); line.setAttribute('y1', 0);
        line.setAttribute('x2', x); line.setAttribute('y2', h - 20);
        line.setAttribute('stroke', '#b94a48');
        line.setAttribute('stroke-width', '1.5');
        line.setAttribute('stroke-dasharray', '4 3');
        svgEl2.appendChild(line);

        const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        lbl.setAttribute('x', x + 4);
        lbl.setAttribute('y', 18);
        lbl.setAttribute('class', 'axis-label');
        lbl.setAttribute('fill', '#b94a48');
        lbl.textContent = 'Budget ' + BUDGET;
        svgEl2.appendChild(lbl);
      }
    }
  }

  /* Grid intensity range bar */
  if (gridData) {
    const bars = [
      { label: 'Min',  value: gridData.min_g_per_kwh, color: '#1a6e3e' },
      { label: 'Avg',  value: gridData.avg_g_per_kwh, color: '#2e9e5e' },
      { label: 'Max',  value: gridData.max_g_per_kwh, color: '#8ab8a4' }
    ];
    drawBarChart('svg-grid', bars, Math.max(gridData.max_g_per_kwh * 1.1, 10), 'gCO₂/kWh');
  }

  /* Latency chart */
  if (probeData) {
    const bars = [
      { label: 'Avg latency', value: probeData.avg_latency_ms, color: '#2e9e5e' },
      { label: 'p95 latency', value: probeData.p95_latency_ms, color: '#8ab8a4' }
    ];
    drawBarChart('svg-latency', bars, Math.max(probeData.p95_latency_ms * 1.2, 10), 'ms');
  }

  /* ========================================================
     Evidence provenance panel
     ======================================================== */
  if (provenanceEl) {
    provenance.forEach(item => {
      const card = document.createElement('div');
      card.className = 'provenance-card';

      const fileEl = document.createElement('div');
      fileEl.className = 'provenance-file';
      fileEl.textContent = item.file;

      const descEl = document.createElement('div');
      descEl.className = 'provenance-desc';
      descEl.textContent = item.desc;

      const metaEl = document.createElement('div');
      metaEl.className = 'provenance-meta';
      if (item.lastMod) {
        try {
          metaEl.textContent = 'Last modified: ' + new Date(item.lastMod).toUTCString();
        } catch (_) {
          metaEl.textContent = 'Last modified: ' + item.lastMod;
        }
      } else {
        metaEl.textContent = 'Last modified: not available via fetch headers';
      }

      const statusEl = document.createElement('span');
      statusEl.className = 'provenance-status status-' + item.status;
      statusEl.textContent = item.statusLabel;

      card.appendChild(fileEl);
      card.appendChild(descEl);
      card.appendChild(metaEl);
      card.appendChild(statusEl);
      provenanceEl.appendChild(card);
    });
  }
}

/* ============================================================
   Bootstrap
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  loadAndRender().catch(err => {
    const el = document.getElementById('last-updated-text');
    if (el) el.textContent = 'Error loading evidence: ' + err.message;
    console.error('Dashboard load error:', err);
  });
});
