from pydantic import BaseModel


class EvaluationCreate(BaseModel):
    model_name: str
    dataset_name: str
    version: str


class EvaluationResultCreate(BaseModel):
    expected: str
    actual: str
