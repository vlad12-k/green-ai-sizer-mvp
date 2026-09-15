"""Canonical forecast evidence, shared by carbon calculation and publication."""
import csv
import json
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_grid(root=ROOT, now=None):
    grid = json.loads((root / 'data/grid_intensity_uk_summary.json').read_text())
    with (root / 'data/grid_intensity_uk_snapshot.csv').open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    values = [float(row['carbon_intensity_g_per_kwh']) for row in rows]
    if not values or any(not math.isfinite(v) or v < 0 for v in values):
        raise ValueError('Grid snapshot must contain finite, nonnegative intensities')
    stamps = [datetime.fromisoformat(row['timestamp_from'].replace('Z', '+00:00')) for row in rows]
    if any(t.tzinfo is None for t in stamps) or len(set(stamps)) != len(stamps):
        raise ValueError('Grid timestamps must be unique and timezone-aware')
    expected = {'count_points': len(values), 'min_g_per_kwh': round(min(values), 2),
                'avg_g_per_kwh': round(sum(values) / len(values), 2),
                'max_g_per_kwh': round(max(values), 2)}
    if any(grid.get(key) != value for key, value in expected.items()):
        raise ValueError('Grid summary does not match canonical snapshot')
    generated = datetime.fromisoformat(grid['generated_utc'].replace('Z', '+00:00'))
    if generated.tzinfo is None:
        raise ValueError('Grid generation time must be timezone-aware')
    if now is not None:
        if not timedelta(minutes=-5) <= now - generated <= timedelta(hours=48):
            raise ValueError('Grid evidence is stale or future-dated (48-hour limit)')
        if not now - timedelta(hours=48) <= max(stamps) <= now + timedelta(hours=24):
            raise ValueError('Grid observation window is stale or invalid')
    return grid


def sync_evidence(root=ROOT, check=False):
    load_grid(root)
    for source in ('data/grid_intensity_uk_summary.json', 'data/scenario-baseline-improved.csv',
                   'scripts/probe_run_summary.json'):
        src = root / source
        dst = root / 'docs/evidence' / src.name
        if check:
            if not dst.exists() or src.read_bytes() != dst.read_bytes():
                raise ValueError(f'Dashboard mirror differs from canonical source: {dst.name}')
        else:
            dst.write_bytes(src.read_bytes())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--fresh', action='store_true')
    args = parser.parse_args()
    load_grid(now=datetime.now(timezone.utc) if args.fresh else None)
    sync_evidence(check=args.check)
