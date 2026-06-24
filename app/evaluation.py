from sentence_transformers import SentenceTransformer
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def calculate_metrics(expected: list[str], actual: list[str]):
    y_true = [1 if x.strip() else 0 for x in expected]
    y_pred = [1 if x.strip() else 0 for x in actual]

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
    }


def semantic_similarity(
    expected_text: str,
    actual_text: str,
):
    expected_embedding = model.encode(
        expected_text
    )

    actual_embedding = model.encode(
        actual_text
    )

    similarity = cosine_similarity(
        [expected_embedding],
        [actual_embedding],
    )[0][0]

    return float(similarity)


def detect_regression(
    baseline_f1: float,
    current_f1: float,
    baseline_similarity: float,
    current_similarity: float,
):
    f1_drop = baseline_f1 - current_f1

    similarity_drop = (
        baseline_similarity - current_similarity
    )

    if f1_drop > 0.05:
        return "FAIL"

    if similarity_drop > 0.10:
        return "FAIL"

    return "PASS"
