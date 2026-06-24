from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import (
    Base,
    engine,
    get_db,
)

from app.schemas import (
    EvaluationCreate,
    EvaluationResultCreate,
)

from app import service

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Regression Validation Framework",
    version="1.0.0",
)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/evaluations")
def create_evaluation(
    payload: EvaluationCreate,
    db: Session = Depends(get_db),
):
    return service.create_evaluation(
        db,
        payload.model_name,
        payload.dataset_name,
        payload.version,
    )


@app.post("/evaluations/{evaluation_id}/results")
def submit_result(
    evaluation_id: UUID,
    payload: EvaluationResultCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.submit_result(
            db,
            evaluation_id,
            payload.expected,
            payload.actual,
        )

    except LookupError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@app.post("/evaluations/{evaluation_id}/evaluate")
def evaluate(
    evaluation_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return service.evaluate_run(
            db,
            evaluation_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@app.get("/evaluations/{evaluation_id}/report")
def get_report(
    evaluation_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return service.get_report(
            db,
            evaluation_id,
        )

    except LookupError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
