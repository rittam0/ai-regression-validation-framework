import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, String, Text, Uuid

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    model_name = Column(String(100), nullable=False)

    dataset_name = Column(String(100), nullable=False)

    version = Column(String(50), nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
    )


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    evaluation_id = Column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    expected = Column(Text, nullable=False)

    actual = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
    )


class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"

    id = Column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    evaluation_id = Column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    precision = Column(Float)

    recall = Column(Float)

    f1_score = Column(Float)

    semantic_similarity = Column(Float)

    regression_status = Column(String(20))

    created_at = Column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
    )
