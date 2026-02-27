import csv
import os
import sys
from typing import Dict, Tuple

BUDGET_G_PER_1K = float(sys.argv[1]) if len(sys.argv) > 1 else 200.0  # default budget


REQUIRED_FIELDS = [
    "scenario",
    "requests_per_day",
    "cache_hit_rate",
    "small_route_rate",
    "wh_small",
    "wh_large",
    "grid_intensity_g_per_kwh",
]


def _to_float(row: Dict[str, str], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid or missing numeric field '{key}' in row: {row}") from e


def calc_row(row: Dict[str, str]) -> Tuple[float, float]:
    """
    Returns:
      g_per_1k: grams CO2e per 1,000 requests
      gco2_total: total grams CO2e per day
    """
    rpd = _to_float(row, "requests_per_day")
    if rpd <= 0:
        raise ValueError(f"requests_per_day must be > 0. Got {rpd} in row: {row}")

    cache_hit = _to_float(row, "cache_hit_rate")         # 0..1
    small_rate = _to_float(row, "small_route_rate")      # 0..1 (of computed requests)
    wh_small = _to_float(row, "wh_small")
    wh_large = _to_float(row, "wh_large")
    ci = _to_float(row, "grid_intensity_g_per_kwh")       # gCO2/kWh

    # basic sanity checks
    if not (0.0 <= cache_hit <= 1.0):
        raise ValueError(f"cache_hit_rate must be in [0,1]. Got {cache_hit} in row: {row}")
    if not (0.0 <= small_rate <= 1.0):
        raise ValueError(f"small_route_rate must be in [0,1]. Got {small_rate} in row: {row}")
    if wh_small < 0 or wh_large < 0:
        raise ValueError(f"wh_small/wh_large must be >= 0. Got {wh_small}/{wh_large} in row: {row}")
    if ci < 0:
        raise ValueError(f"grid_intensity_g_per_kwh must be >= 0. Got {ci} in row: {row}")

    computed = rpd * (1.0 - cache_hit)
    small = computed * small_rate
    large = computed * (1.0 - small_rate)

    wh_total = small * wh_small + large * wh_large
    kwh_total = wh_total / 1000.0
    gco2_total = kwh_total * ci

    g_per_1k = gco2_total / (rpd / 1000.0)
    return g_per_1k, gco2_total


def write_step_summary(lines: str) -> None:
    """
    Writes a Markdown summary in GitHub Actions UI if available.
    Safe to call locally (does nothing).
    """
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write(lines)


def main() -> None:
    path = "workbook/appendix-d-baseline-improved.csv"

    # Read CSV
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"ERROR: CSV not found at '{path}'.")
        sys.exit(1)

    # Validate headers
    if not rows:
        print("ERROR: CSV is empty.")
        sys.exit(1)

    missing_headers = [h for h in REQUIRED_FIELDS if h not in rows[0].keys()]
    if missing_headers:
        print(f"ERROR: CSV missing required headers: {missing_headers}")
        sys.exit(1)

    # Compute scenarios
    results: Dict[str, Tuple[float, float]] = {}
    for row in rows:
        # skip blank rows
        if not row.get("requests_per_day"):
            continue

        scenario = (row.get("scenario") or "").strip().lower()
        if not scenario:
            continue

        try:
            g_per_1k, g_total = calc_row(row)
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(1)

        results[scenario] = (g_per_1k, g_total)

    if "improved" not in results:
        print("ERROR: No 'improved' row found (or requests_per_day is empty). Please fill it in the CSV.")
        sys.exit(1)

    improved_g_per_1k, improved_g_total = results["improved"]
    baseline_g_per_1k, baseline_g_total = results.get("baseline", (None, None))

    # Console output (visible in logs)
    print(f"Budget (gCO2e/1k): {BUDGET_G_PER_1K:.2f}")
    if baseline_g_per_1k is not None:
        print(f"Baseline gCO2e per 1k requests: {baseline_g_per_1k:.2f} gCO2e")
        print(f"Baseline total gCO2e/day: {baseline_g_total:.2f} gCO2e")
    print(f"Improved gCO2e per 1k requests: {improved_g_per_1k:.2f} gCO2e")
    print(f"Improved total gCO2e/day: {improved_g_total:.2f} gCO2e")

    # GitHub Step Summary (nice UI block)
    md = "## Carbon Budget Gate — Results\n"
    md += f"- **Budget:** `{BUDGET_G_PER_1K:.2f}` gCO₂e / 1k requests\n"
    if baseline_g_per_1k is not None:
        md += f"- **Baseline:** `{baseline_g_per_1k:.2f}` gCO₂e / 1k (total/day: `{baseline_g_total:.2f}` g)\n"
    md += f"- **Improved:** `{improved_g_per_1k:.2f}` gCO₂e / 1k (total/day: `{improved_g_total:.2f}` g)\n"
    if baseline_g_per_1k is not None and baseline_g_per_1k > 0:
        reduction = (1 - (improved_g_per_1k / baseline_g_per_1k)) * 100
        md += f"- **Estimated reduction vs baseline:** `{reduction:.1f}%`\n"
    write_step_summary(md)

    # Budget gate
    if improved_g_per_1k > BUDGET_G_PER_1K:
        print(f"FAIL: Budget exceeded (improved={improved_g_per_1k:.2f} > budget={BUDGET_G_PER_1K:.2f}).")
        sys.exit(2)

    print("PASS: Within budget.")
    sys.exit(0)


if __name__ == "__main__":
    main()
