"""Reproducible training on authored synthetic routing examples only."""
import csv
from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'data/router_train.csv'
MODEL_PATH = ROOT / 'app/ml/router_model.joblib'


def load_data(path=DATA_PATH):
    with path.open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    if not rows or any(not r['text'].strip() or r['label'] not in ('small', 'large') for r in rows):
        raise ValueError('Invalid routing dataset')
    texts = [r['text'].strip() for r in rows]
    if len(set(t.lower() for t in texts)) != len(texts):
        raise ValueError('Duplicate routing examples')
    return texts, [r['label'] for r in rows]


def train():
    texts, labels = load_data()
    model = Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
                      ('clf', LogisticRegression(max_iter=1000, random_state=42))])
    model.fit(texts, labels)
    return model


if __name__ == '__main__':
    joblib.dump(train(), MODEL_PATH)
    print(f'Saved {MODEL_PATH.name}')
