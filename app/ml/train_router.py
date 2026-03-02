import csv
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

DATA_PATH = Path("data/route_training.csv")
MODEL_PATH = Path("app/ml/router_model.joblib")

def load_data():
    texts, labels = [], []
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = (row.get("text") or "").strip()
            y = (row.get("label") or "").strip()
            if t and y:
                texts.append(t)
                labels.append(y)
    return texts, labels

def main():
    X, y = load_data()
    if len(X) < 20:
        print(f"WARNING: dataset is small ({len(X)} rows). Add more rows to improve the model.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y if len(set(y))>1 else None)

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    print(classification_report(y_test, preds))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
