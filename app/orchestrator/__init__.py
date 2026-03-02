import json
import random
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except Exception:
        body = {}

    query = (body.get("query") or "").strip()
    seed = body.get("seed", None)
    if seed is not None:
        random.seed(seed)

    cache_hit_rate = float(body.get("cache_hit_rate", 0.30))
    small_route_rate = float(body.get("small_route_rate", 0.70))
    wh_small = float(body.get("wh_small", 0.2))
    wh_large = float(body.get("wh_large", 2.0))

    if not query:
        return func.HttpResponse(
            json.dumps({"ok": True, "message": "POST JSON with 'query'."}),
            status_code=200,
            mimetype="application/json"
        )

    cache_hit_rate = max(0.0, min(1.0, cache_hit_rate))
    small_route_rate = max(0.0, min(1.0, small_route_rate))

    cache_hit = random.random() < cache_hit_rate
    route = "small" if (len(query) <= 40 or random.random() < small_route_rate) else "large"

    base = 25 if cache_hit else 60
    route_penalty = 20 if route == "small" else 120
    latency_ms = base + route_penalty + random.randint(0, 25)

    wh_request = 0.02 if cache_hit else (wh_small if route == "small" else wh_large)

    return func.HttpResponse(
        json.dumps({
            "query_len": len(query),
            "cache_hit": cache_hit,
            "route": route,
            "latency_ms": latency_ms,
            "wh_request": wh_request
        }),
        status_code=200,
        mimetype="application/json"
    )
