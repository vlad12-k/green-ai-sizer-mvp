import csv
import sys

BUDGET_G_PER_1K = float(sys.argv[1]) if len(sys.argv) > 1 else 200.0  # adjust later

def calc_row(row):
    # Required fields
    rpd = float(row["requests_per_day"])
    cache_hit = float(row["cache_hit_rate"])       # 0..1
    small_rate = float(row["small_route_rate"])    # 0..1 (of computed requests)
    wh_small = float(row["wh_small"])
    wh_large = float(row["wh_large"])
    ci = float(row["grid_intensity_g_per_kwh"])

    computed = rpd * (1.0 - cache_hit)
    small = computed * small_rate
    large = computed * (1.0 - small_rate)

    wh_total = small * wh_small + large * wh_large
    kwh_total = wh_total / 1000.0
    gco2_total = kwh_total * ci

    g_per_1k = gco2_total / (rpd / 1000.0)
    return g_per_1k, gco2_total

def main():
    path = "workbook/appendix-d-baseline-improved.csv"
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    results = {}
    for row in rows:
        if not row["requests_per_day"]:
            continue
        scenario = row["scenario"].strip()
        g_per_1k, g_total = calc_row(row)
        results[scenario] = (g_per_1k, g_total)

    if "improved" not in results:
        print("No 'improved' row filled yet. Please add values in the CSV.")
        sys.exit(1)

    g_per_1k, _ = results["improved"]
    print(f"Improved gCO2e per 1k requests: {g_per_1k:.2f} gCO2e")

    if g_per_1k > BUDGET_G_PER_1K:
        print(f"FAIL: Budget exceeded (budget={BUDGET_G_PER_1K} gCO2e/1k).")
        sys.exit(2)

    print(f"PASS: Within budget (budget={BUDGET_G_PER_1K} gCO2e/1k).")

if __name__ == "__main__":
    main()
