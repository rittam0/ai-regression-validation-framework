from uuid import UUID

from sqlalchemy.orm import Session

from app import repository
from app.evaluation import (
    calculate_metrics,
    semantic_similarity,
    detect_regression,
)


def create_evaluation(
    db: Session,
    model_name: str,
    dataset_name: str,
    version: str,
):
    return repository.create_evaluation(
        db,
        model_name,
        dataset_name,
        version,
    )


def submit_result(
    db: Session,
    evaluation_id: UUID,
    expected: str,
    actual: str,
):
    evaluation = repository.get_evaluation(
        db,
        evaluation_id,
    )

    if not evaluation:
        raise LookupError(
            "Evaluation not found"
        )

    return repository.create_result(
        db,
        evaluation_id,
        expected,
        actual,
    )


def evaluate_run(
    db: Session,
    evaluation_id: UUID,
):
    results = repository.get_results(
        db,
        evaluation_id,
    )

    if not results:
        raise ValueError(
            "No results submitted"
        )

    expected = [
        r.expected
        for r in results
    ]

    actual = [
        r.actual
        for r in results
    ]

    metrics = calculate_metrics(
        expected,
        actual,
    )

    similarities = [
        semantic_similarity(
            r.expected,
            r.actual,
        )
        for r in results
    ]

    avg_similarity = (
        sum(similarities)
        / len(similarities)
    )

    status = detect_regression(
        baseline_f1=1.0,
        current_f1=metrics["f1_score"],
        baseline_similarity=1.0,
        current_similarity=avg_similarity,
    )

    return repository.create_report(
        db,
        evaluation_id,
        precision=metrics["precision"],
        recall=metrics["recall"],
        f1_score=metrics["f1_score"],
        semantic_similarity=avg_similarity,
        regression_status=status,
    )


def get_report(
    db: Session,
    evaluation_id: UUID,
):
    report = repository.get_report(
        db,
        evaluation_id,
    )

    if not report:
        raise LookupError(
            "Report not found"
        )

    return report
