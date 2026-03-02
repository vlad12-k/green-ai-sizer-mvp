from pathlib import Path
import re
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "router_model.joblib"

# Safety / governance rules (override ML when high-risk)
FORCE_LARGE_PATTERNS = [
    r"\b(emergency|escalation|outage|incident response|ransomware)\b",
    r"\b(trade[- ]?off|compare|evaluate|critically|governance)\b",
    r"\b(roadmap|stakeholder|raci|policy)\b",
]

FORCE_SMALL_PATTERNS = [
    r"\b(define|what is|meaning of)\b",
    r"\b(short summary|summarise|summary)\b",
]

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}. Run: python app/ml/train_router.py")
    return joblib.load(MODEL_PATH)

_MODEL = None

def predict_route(text: str) -> str:
    global _MODEL
    t = (text or "").strip().lower()

    # Rule overrides first (safety)
    for p in FORCE_LARGE_PATTERNS:
        if re.search(p, t):
            return "large"

    for p in FORCE_SMALL_PATTERNS:
        if re.search(p, t) and len(t) < 120:
            return "small"

    # ML fallback
    if _MODEL is None:
        _MODEL = load_model()

    return _MODEL.predict([text])[0]
