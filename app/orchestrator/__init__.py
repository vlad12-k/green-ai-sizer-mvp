import json
import random
import azure.functions as func

from app.ml.router import predict_route


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except Exception:
        body = {}

    query = (body.get("query") or "").strip()
    force = (body.get("force") or "").strip().lower()  # "small" | "large"
    seed = body.get("seed", None)

    if seed is not None:
        random.seed(seed)

    # Tunable knobs (proxy inputs for workbook)
    cache_hit_rate = float(body.get("cache_hit_rate", 0.30))
    wh_small = float(body.get("wh_small", 0.2))
    wh_large = float(body.get("wh_large", 2.0))

    if not query:
        return func.HttpResponse(
            json.dumps({"ok": True, "message": "POST JSON with 'query'."}),
            status_code=200,
            mimetype="application/json"
        )

    cache_hit_rate = max(0.0, min(1.0, cache_hit_rate))
    cache_hit = random.random() < cache_hit_rate

    # Route decision: forced override OR ML router
    if force in ("small", "large"):
        route = force
    else:
        route = predict_route(query)   # <-- REAL ML decision + safety rules

    # Latency simulation (ms) - still proxy, but route is real
    base = 25 if cache_hit else 60
    route_penalty = 20 if route == "small" else 120
    latency_ms = base + route_penalty + random.randint(0, 25)

    # Energy proxy per request (Wh)
    wh_request = 0.02 if cache_hit else (wh_small if route == "small" else wh_large)

    return func.HttpResponse(
        json.dumps({
            "query_len": len(query),
            "cache_hit": cache_hit,
            "route": route,
            "latency_ms": latency_ms,
            "wh_request": wh_request,
            "notes": "Rule-assisted ML router (scikit-learn) + cache simulation. Energy remains proxy."
        }),
        status_code=200,
        mimetype="application/json"
    )
