from app.evaluation import detect_regression


def test_small_f1_drop_passes():
    assert (
        detect_regression(
            baseline_f1=1.0,
            current_f1=0.96,
            baseline_similarity=1.0,
            current_similarity=0.95,
        )
        == "PASS"
    )


def test_large_f1_drop_fails():
    assert (
        detect_regression(
            baseline_f1=1.0,
            current_f1=0.80,
            baseline_similarity=1.0,
            current_similarity=1.0,
        )
        == "FAIL"
    )


def test_small_similarity_drop_passes():
    assert (
        detect_regression(
            baseline_f1=1.0,
            current_f1=1.0,
            baseline_similarity=1.0,
            current_similarity=0.95,
        )
        == "PASS"
    )


def test_large_similarity_drop_fails():
    assert (
        detect_regression(
            baseline_f1=1.0,
            current_f1=1.0,
            baseline_similarity=1.0,
            current_similarity=0.70,
        )
        == "FAIL"
    )
