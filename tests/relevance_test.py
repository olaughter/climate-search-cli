import pickle

from cs.output import build_policy_sequence
from cs.relevance import transform_for_relevance


def test_transform_for_relevance():
    with open("tests/fixtures/rows", "rb") as f:
        rows = pickle.load(f)
    policies = build_policy_sequence(rows)
    keywords = ("forests",)

    results = transform_for_relevance(rows, keywords, policies)

    assert len(results) == len(rows) == len(policies)
