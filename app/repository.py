from uuid import UUID

from sqlalchemy.orm import Session

from app.models import (
    EvaluationRun,
    EvaluationResult,
    EvaluationReport,
)


def create_evaluation(
    db: Session,
    model_name: str,
    dataset_name: str,
    version: str,
):
    evaluation = EvaluationRun(
        model_name=model_name,
        dataset_name=dataset_name,
        version=version,
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    return evaluation


def get_evaluation(
    db: Session,
    evaluation_id: UUID,
):
    return (
        db.query(EvaluationRun)
        .filter(EvaluationRun.id == evaluation_id)
        .first()
    )


def create_result(
    db: Session,
    evaluation_id: UUID,
    expected: str,
    actual: str,
):
    result = EvaluationResult(
        evaluation_id=evaluation_id,
        expected=expected,
        actual=actual,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result


def get_results(
    db: Session,
    evaluation_id: UUID,
):
    return (
        db.query(EvaluationResult)
        .filter(
            EvaluationResult.evaluation_id == evaluation_id
        )
        .all()
    )


def create_report(
    db: Session,
    evaluation_id: UUID,
    precision: float,
    recall: float,
    f1_score: float,
    semantic_similarity: float,
    regression_status: str,
):
    report = EvaluationReport(
        evaluation_id=evaluation_id,
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        semantic_similarity=semantic_similarity,
        regression_status=regression_status,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


def get_report(
    db: Session,
    evaluation_id: UUID,
):
    return (
        db.query(EvaluationReport)
        .filter(
            EvaluationReport.evaluation_id == evaluation_id
        )
        .first()
    )
