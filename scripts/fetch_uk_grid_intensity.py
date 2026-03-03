import csv
import json
import statistics
import urllib.request
from datetime import datetime, timezone

API_24H = "https://api.carbonintensity.org.uk/intensity/date"

def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "green-ai-sizer-mvp"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    payload = fetch_json(API_24H)
    rows = payload.get("data", [])

    if not rows:
        raise SystemExit("No data returned from UK Carbon Intensity API.")

    # Extract (timestamp, intensity.forecast)
    points = []
    for item in rows:
        ts = item.get("from")
        intensity = (item.get("intensity") or {}).get("forecast")
        if ts and intensity is not None:
            points.append((ts, float(intensity)))

    values = [v for _, v in points]
    min_v = min(values)
    max_v = max(values)
    avg_v = statistics.mean(values)

    # Save snapshot
    out_csv = "data/grid_intensity_uk_snapshot.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp_from", "region", "carbon_intensity_g_per_kwh", "source"])
        for ts, v in points:
            w.writerow([ts, "UK", f"{v:.2f}", "NESO/UK Carbon Intensity API (forecast)"])

    # Save summary (min/avg/max)
    out_summary = "data/grid_intensity_uk_summary.json"
    summary = {
        "region": "UK",
        "source": "NESO/UK Carbon Intensity API",
        "window": "last_24h (half-hourly)",
        "count_points": len(values),
        "min_g_per_kwh": round(min_v, 2),
        "avg_g_per_kwh": round(avg_v, 2),
        "max_g_per_kwh": round(max_v, 2),
        "generated_utc": datetime.now(timezone.utc).isoformat()
    }
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Saved:", out_csv)
    print("Saved:", out_summary)
    print("Summary:", summary)

if __name__ == "__main__":
    main()
