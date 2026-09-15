"""Explainable hybrid routing. Scores are uncalibrated classifier probabilities."""
from pathlib import Path
import re
import joblib

MODEL_PATH = Path(__file__).resolve().parent / 'router_model.joblib'
FORCE_LARGE_PATTERNS = [
    r'\b(emergency|escalation|outage|incident response|ransomware)\b',
    r'\b(trade[- ]?off|compare|evaluate|critically|governance)\b',
    r'\b(roadmap|stakeholder|raci|policy|design|diagnos\w*|treatment)\b',
]
FORCE_SMALL_PATTERNS = [r'\b(define|what is|meaning of|short summary|summarise|summary)\b']
_MODEL = None


def load_model():
    return joblib.load(MODEL_PATH)


def route_request(text, *, sensitive=False, threshold=0.65):
    global _MODEL
    if not isinstance(text, str) or not text.strip() or len(text) > 20000:
        raise ValueError('query must contain 1 to 20000 characters')
    if not 0.5 <= threshold <= 1:
        raise ValueError('threshold must be between 0.5 and 1')
    decision = {'route': 'large', 'confidence': None, 'reason': '', 'policy_overrides': [],
                'router_version': '2', 'confidence_kind': 'not_applicable'}
    def result(route, reason, policy=False):
        decision.update(route=route, reason=reason)
        if policy:
            decision['policy_overrides'].append(reason)
        return decision
    if sensitive:
        return result('reject', 'sensitive_request_requires_approved_runtime', True)
    t = text.strip().lower()
    if any(re.search(p, t) for p in FORCE_LARGE_PATTERNS):
        return result('large', 'high_complexity_policy', True)
    if len(t) < 120 and any(re.search(p, t) for p in FORCE_SMALL_PATTERNS):
        return result('small', 'simple_request_policy', True)
    try:
        if _MODEL is None:
            _MODEL = load_model()
        probabilities = _MODEL.predict_proba([text])[0]
        index = int(probabilities.argmax())
        confidence = float(probabilities[index])
        decision.update(confidence=confidence, confidence_kind='uncalibrated_probability')
        if confidence < threshold:
            return result('large', 'low_confidence_fallback')
        return result(str(_MODEL.classes_[index]), 'ml_prediction')
    except (OSError, ValueError, EOFError):
        return result('large', 'model_unavailable_fallback')


def predict_route(text):
    """Compatibility adapter for callers expecting a small/large string."""
    return route_request(text)['route']
