from cardiorisk.evaluate import evaluate  # noqa: E402


def test_roc_auc():
    auc = evaluate(seed=0)
    assert auc >= 0.85
