import json
import os
import statistics
import time
import urllib.request
import urllib.error

URL = os.environ.get("URL", "").strip()
if not URL:
    raise SystemExit("URL is not set. Run: source .env && export URL")

N = int(os.environ.get("N", "200"))
SLEEP = float(os.environ.get("SLEEP", "0.05"))
TIMEOUT = float(os.environ.get("TIMEOUT", "60"))
RETRIES = int(os.environ.get("RETRIES", "3"))
RETRY_BACKOFF = float(os.environ.get("RETRY_BACKOFF", "1.5"))

QUERIES = [
    "what is the heatwave incident checklist",
    "current grid carbon intensity",
    "summarise heat-health advice for staff",
    "compare mitigation strategies under heat stress",
    "map stakeholders and propose a RACI for sustainable AI governance",
]

def post(payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(RETRY_BACKOFF * attempt)

    raise last_err  # after retries

def main():
    routes, cache_hits, latencies, whs = [], [], [], []
    failures = 0

    for i in range(N):
        q = QUERIES[i % len(QUERIES)]
        try:
            out = post({"query": q, "seed": i})
        except Exception as e:
            failures += 1
            # record a "failure" datapoint but keep going
            routes.append("error")
            cache_hits.append(False)
            latencies.append(float(TIMEOUT * 1000))
            whs.append(0.0)
            continue

        routes.append(out.get("route"))
        cache_hits.append(bool(out.get("cache_hit")))
        latencies.append(float(out.get("latency_ms", 0)))
        whs.append(float(out.get("wh_request", 0)))

        time.sleep(SLEEP)

    ok_n = N - failures
    cache_rate = sum(cache_hits) / len(cache_hits)
    small_rate = sum(1 for r in routes if r == "small") / len(routes)

    p95 = statistics.quantiles(latencies, n=20)[18]

    summary = {
        "n": N,
        "ok_responses": ok_n,
        "failures": failures,
        "cache_hit_rate_observed": round(cache_rate, 4),
        "small_route_rate_observed": round(small_rate, 4),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "p95_latency_ms": round(p95, 2),
        "avg_wh_request": round(sum(whs) / len(whs), 4),
        "timeout_s": TIMEOUT,
        "retries": RETRIES,
    }

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
