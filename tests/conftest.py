import os
import sys
import types
from pathlib import Path

import pytest

TEST_DB = Path(__file__).resolve().parent / "test_evaluation.db"

os.environ.setdefault(
    "DATABASE_URL",
    f"sqlite:///{TEST_DB}",
)


class FakeSentenceTransformer:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name

    def encode(self, text: str):
        seed = sum(ord(char) for char in text)

        return [
            float((seed + offset) % 17)
            for offset in range(8)
        ]


sentence_transformers = types.ModuleType("sentence_transformers")
sentence_transformers.SentenceTransformer = FakeSentenceTransformer
sys.modules["sentence_transformers"] = sentence_transformers


@pytest.fixture(autouse=True)
def mock_sentence_transformer(monkeypatch):
    from app import evaluation

    evaluation.get_model.cache_clear()
    monkeypatch.setattr(
        evaluation,
        "get_model",
        lambda: FakeSentenceTransformer(),
    )
