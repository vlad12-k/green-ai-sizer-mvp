# Router v2 model card

The router selects a simulated small or large route. It does not call an LLM,
measure answer quality, detect all sensitive data, or provide clinical advice.
Explicit `sensitive: true` requests are rejected until an approved runtime exists;
this flag is an integration contract, not a privacy classifier.

Order: explicit sensitivity policy → high-complexity policy → simple-request
policy → TF-IDF/logistic regression → confidence threshold (0.65) → large fallback.
A high-complexity policy decision bypasses simulated cache. Policy decisions cannot be overridden by force.
`predict_route` retains the legacy string interface. The HTTP response adds
`decision` and `simulation: true`; legacy route/latency/energy fields remain.
Latency, cache hits and energy are simulated. No cost or carbon estimates are
invented inside a routing decision without the required runtime inputs.

`confidence` is null for rules and an uncalibrated probability for ML decisions.
It must not be interpreted as the probability of a correct LLM answer. Missing
models fall back to large; corrupt or incompatible artifacts may still require
operator intervention. Only the repository-controlled model is loaded with joblib.

## Data and reproduction

`data/router_train.csv` has 40 authored synthetic examples. `router_eval.csv`
has 20 separately authored, non-overlapping examples.
No real user prompts or third-party text were copied into the new fixtures.
These small synthetic fixtures check regressions; they cannot establish
production routing quality, fairness, privacy, or generalization.

Install `app/requirements.txt`, then run:

```sh
python app/ml/train_router.py
python scripts/evaluate_router.py --write
make verify-release
```

The evaluator checks overlap, rebuilds the model, compares probabilities,
reports hybrid and classifier-only accuracy, large-route recall, confusion
matrix, decision reasons and failed examples. The regression gate requires
large-route recall >= 0.8 on this fixture. Evaluation evidence includes dataset
hashes and must match a fresh run. Production qualification requires a larger,
independently labelled workload set and measured answer quality/cost/latency.
