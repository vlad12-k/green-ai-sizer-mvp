"""Evaluate the complete router and the classifier on a held-out synthetic fixture."""
import hashlib
import json
import sys
from pathlib import Path
from collections import Counter
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from ml import router
from ml.train_router import load_data, train


def evaluate():
    train_texts, _ = load_data(ROOT / 'data/router_train.csv')
    texts, labels = load_data(ROOT / 'data/router_eval.csv')
    if set(t.lower() for t in texts) & set(t.lower() for t in train_texts):
        raise ValueError('Train/evaluation overlap')
    model = joblib.load(router.MODEL_PATH)
    rebuilt = train()
    import numpy as np
    if not np.allclose(model.predict_proba(texts), rebuilt.predict_proba(texts), atol=1e-10):
        raise ValueError('Committed model differs from reproducible training')
    router._MODEL = model
    decisions = [router.route_request(t) for t in texts]
    predictions = [d['route'] for d in decisions]
    report = {
        'dataset_kind': 'authored synthetic fixture; not production or answer-quality evidence',
        'train_count': len(train_texts), 'evaluation_count': len(texts),
        'labels': ['small', 'large'], 'threshold': 0.65,
        'accuracy': accuracy_score(labels, predictions),
        'classifier_only_accuracy': accuracy_score(labels, model.predict(texts)),
        'large_recall': recall_score(labels, predictions, pos_label='large'),
        'confusion_matrix': confusion_matrix(labels, predictions, labels=['small', 'large']).tolist(),
        'decision_reasons': dict(Counter(d['reason'] for d in decisions)),
        'failures': [{'text': t, 'expected': y, 'actual': p} for t,y,p in zip(texts, labels, predictions) if y != p],
        'dataset_sha256': {name: hashlib.sha256((ROOT / 'data' / name).read_bytes()).hexdigest()
                           for name in ('router_train.csv', 'router_eval.csv')},
    }
    if report['large_recall'] < 0.8:
        raise ValueError('Synthetic regression gate: large-route recall below 0.8')
    return report


if __name__ == '__main__':
    result = evaluate()
    serialized = json.dumps(result, indent=2) + '\n'
    path = ROOT / 'docs/evidence/router_evaluation.json'
    if '--write' in sys.argv:
        path.write_text(serialized)
    elif json.loads(path.read_text()) != result:
        raise SystemExit('Evaluation report is stale; regenerate with --write')
    print(serialized)
