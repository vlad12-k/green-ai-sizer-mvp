import csv
import json
import sys
from pathlib import Path


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    grid = repo_root / "docs" / "evidence" / "grid_intensity_uk_summary.json"
    probe = repo_root / "docs" / "evidence" / "probe_run_summary.json"
    scenario = repo_root / "docs" / "evidence" / "scenario-baseline-improved.csv"

    for p in [grid, probe, scenario]:
        if not p.exists():
            fail(f"missing required evidence file: {p}")

    try:
        grid_data = json.loads(grid.read_text(encoding="utf-8"))
        probe_data = json.loads(probe.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"malformed JSON: {e}")

    for key in ["min_g_per_kwh", "avg_g_per_kwh", "max_g_per_kwh", "generated_utc"]:
        if key not in grid_data:
            fail(f"grid summary missing key: {key}")

    for key in ["cache_hit_rate_observed", "small_route_rate_observed"]:
        if key not in probe_data:
            fail(f"probe summary missing key: {key}")

    with scenario.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    if not rows:
        fail("scenario CSV is empty")

    required_headers = [
        "scenario",
        "requests_per_day",
        "cache_hit_rate",
        "small_route_rate",
        "wh_small",
        "wh_large",
        "grid_intensity_g_per_kwh",
    ]
    missing = [h for h in required_headers if h not in rows[0].keys()]
    if missing:
        fail(f"scenario CSV missing headers: {missing}")

    scenarios = {(r.get("scenario") or "").strip().lower() for r in rows}
    if "improved" not in scenarios:
        fail("scenario CSV missing improved row")

    print("OK: evidence valid")


if __name__ == "__main__":
    main()
