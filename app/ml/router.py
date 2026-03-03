from pathlib import Path
import re
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "router_model.joblib"

FORCE_LARGE_PATTERNS = [
    r"\b(emergency|escalation|outage|incident response|ransomware)\b",
    r"\b(trade[- ]?off|compare|evaluate|critically|governance)\b",
    r"\b(roadmap|stakeholder|raci|policy)\b",
]

FORCE_SMALL_PATTERNS = [
    r"\b(define|what is|meaning of)\b",
    r"\b(short summary|summarise|summary)\b",
]

_MODEL = None

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def predict_route(text: str) -> str:
    global _MODEL
    t = (text or "").strip().lower()

    for p in FORCE_LARGE_PATTERNS:
        if re.search(p, t):
            return "large"

    for p in FORCE_SMALL_PATTERNS:
        if re.search(p, t) and len(t) < 120:
            return "small"

    if _MODEL is None:
        _MODEL = load_model()

    return _MODEL.predict([text])[0]

    return _MODEL.predict([text])[0]
