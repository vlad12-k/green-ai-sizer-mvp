import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import azure.functions as func
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from ml import router
from orchestrator import main


class FakeModel:
    classes_ = np.array(['large', 'small'])
    def __init__(self, probabilities):
        self.probabilities = probabilities
    def predict_proba(self, texts):
        return np.array([self.probabilities])


class RouterTests(unittest.TestCase):
    def test_policy_precedes_simple_rule_and_model(self):
        with patch.object(router, 'load_model', side_effect=AssertionError('must not load')):
            self.assertEqual(router.route_request('What is ransomware response')['route'], 'large')
            self.assertEqual(router.route_request('Define cache')['route'], 'small')
            self.assertEqual(router.route_request('Define cache', sensitive=True)['route'], 'reject')

    def test_confidence_and_fallback(self):
        with patch.object(router, '_MODEL', FakeModel([0.2, 0.8])):
            result = router.route_request('Alphabetize these words')
            self.assertEqual(result['route'], 'small')
            self.assertEqual(result['confidence'], 0.8)
        with patch.object(router, '_MODEL', FakeModel([0.49, 0.51])):
            self.assertEqual(router.route_request('A vague request')['reason'], 'low_confidence_fallback')
        with patch.object(router, '_MODEL', None), patch.object(router, 'load_model', side_effect=FileNotFoundError):
            self.assertEqual(router.route_request('A vague request')['reason'], 'model_unavailable_fallback')

    def test_invalid_query(self):
        for query in ('', None, 'x' * 20001):
            with self.assertRaises(ValueError):
                router.route_request(query)

    def call(self, body):
        req = func.HttpRequest(method='POST', url='http://localhost/api/orchestrator', body=json.dumps(body).encode())
        return main(req)

    def test_runtime_labels_simulation_and_preserves_response(self):
        body = {'query':'Define throughput','seed':42}
        response = self.call(body)
        result = json.loads(response.get_body())
        self.assertTrue(result['simulation'])
        self.assertIn('wh_request', result)
        self.assertEqual(result['route'], result['decision']['route'])
        self.assertEqual(response.get_body(), self.call(body).get_body())

    def test_policy_cannot_be_overridden_by_force_or_cache(self):
        result = json.loads(self.call({'query':'Design emergency response','force':'small','cache_hit_rate':1}).get_body())
        self.assertEqual(result['route'], 'large')
        self.assertFalse(result['cache_hit'])
        self.assertEqual(self.call({'query':'hello','sensitive':True,'force':'small'}).status_code, 403)

    def test_bad_runtime_input(self):
        for body in ([], {'query':4}, {'query':'hello', 'wh_small':'NaN'}, {'query':'hello','cache_hit_rate':2}):
            self.assertEqual(self.call(body).status_code, 400)
