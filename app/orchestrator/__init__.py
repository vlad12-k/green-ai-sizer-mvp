import json
import random
import azure.functions as func

from ml.router import route_request


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except Exception:
        return func.HttpResponse("Invalid JSON", status_code=400)

    if not isinstance(body, dict):
        return func.HttpResponse("JSON body must be an object", status_code=400)
    if not isinstance(body.get("query", ""), str):
        return func.HttpResponse("query must be a string", status_code=400)

    query = (body.get("query") or "").strip()
    force = body.get("force", "")  # Simulation override; cannot bypass policy.
    if force not in ("", "small", "large"):
        return func.HttpResponse("Invalid force route", status_code=400)
    seed = body.get("seed", None)

    if seed is not None and not isinstance(seed, (int, str)):
        return func.HttpResponse("Invalid seed", status_code=400)
    rng = random.Random(seed)

    try:
        import math
        cache_hit_rate = float(body.get("cache_hit_rate", 0.30))
        wh_small = float(body.get("wh_small", 0.2))
        wh_large = float(body.get("wh_large", 2.0))
        if not all(math.isfinite(v) for v in (cache_hit_rate, wh_small, wh_large)) or not 0 <= cache_hit_rate <= 1 or min(wh_small, wh_large) < 0:
            raise ValueError()
        sensitive = body.get("sensitive", False)
        if not isinstance(sensitive, bool):
            raise ValueError()
    except (ValueError, TypeError):
        return func.HttpResponse("Invalid simulation inputs", status_code=400)

    if not query:
        return func.HttpResponse(
            json.dumps({"ok": True, "message": "POST JSON with 'query'."}),
            status_code=200,
            mimetype="application/json"
        )

    cache_hit_rate = max(0.0, min(1.0, cache_hit_rate))
    cache_hit = rng.random() < cache_hit_rate

    try:
        decision = route_request(query, sensitive=sensitive)
    except ValueError as exc:
        return func.HttpResponse(str(exc), status_code=400)
    if decision['route'] == 'reject':
        return func.HttpResponse(json.dumps({'decision': decision, 'simulation': True}), status_code=403, mimetype='application/json')
    route = decision['route']
    if force and not decision['policy_overrides']:
        route = force
        decision.update(route=route, reason='simulation_override', confidence=None, confidence_kind='not_applicable')
    if decision['reason'] == 'high_complexity_policy':
        cache_hit = False

    base = 25 if cache_hit else 60
    route_penalty = 20 if route == "small" else 120
    latency_ms = base + route_penalty + rng.randint(0, 25)

    wh_request = 0.02 if cache_hit else (wh_small if route == "small" else wh_large)

    return func.HttpResponse(
        json.dumps({
            "query_len": len(query),
            "simulation": True,
            "decision": decision,
            "cache_hit": cache_hit,
            "route": route,
            "latency_ms": latency_ms,
            "wh_request": wh_request
        }),
        status_code=200,
        mimetype="application/json"
    )
