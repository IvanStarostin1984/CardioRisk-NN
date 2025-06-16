from cardiorisk import train  # noqa: E402
from cardiorisk import evaluate  # noqa: E402


def test_imports():
    assert hasattr(train, "main")
    assert hasattr(evaluate, "main")
