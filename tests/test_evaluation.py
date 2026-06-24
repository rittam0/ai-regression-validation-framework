from app.evaluation import (
    calculate_metrics,
    semantic_similarity,
    detect_regression,
)


def test_metrics_perfect_match():
    result = calculate_metrics(
        ["VPN issue"],
        ["VPN issue"],
    )

    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1_score"] == 1.0


def test_semantic_similarity_identical():
    score = semantic_similarity(
        "VPN access unavailable",
        "VPN access unavailable",
    )

    assert score > 0.95


def test_regression_pass():
    status = detect_regression(
        baseline_f1=1.0,
        current_f1=0.98,
        baseline_similarity=1.0,
        current_similarity=0.95,
    )

    assert status == "PASS"


def test_regression_fail_f1():
    status = detect_regression(
        baseline_f1=1.0,
        current_f1=0.80,
        baseline_similarity=1.0,
        current_similarity=1.0,
    )

    assert status == "FAIL"


def test_regression_fail_similarity():
    status = detect_regression(
        baseline_f1=1.0,
        current_f1=1.0,
        baseline_similarity=1.0,
        current_similarity=0.70,
    )

    assert status == "FAIL"
