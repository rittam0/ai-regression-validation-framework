# Architecture

```text
                        +------------------+
                        |      Client      |
                        +--------+---------+
                                 |
                                 v
                        +------------------+
                        |     FastAPI      |
                        +--------+---------+
                                 |
                                 v
                        +------------------+
                        |   Service Layer  |
                        +--------+---------+
                                 |
                +----------------+----------------+
                |                                 |
                v                                 v
     +-------------------+          +----------------------+
     | Evaluation Engine |          | PostgreSQL Database |
     +---------+---------+          +----------------------+
               |
               v
     +-------------------+
     | Metrics Engine    |
     | Precision         |
     | Recall            |
     | F1 Score          |
     +---------+---------+
               |
               v
     +-------------------+
     | Semantic Similarity|
     | SentenceTransformer|
     +---------+----------+
               |
               v
     +-------------------+
     | Regression Logic  |
     | PASS / FAIL       |
     +-------------------+
```

## Components

### FastAPI

Provides REST endpoints and API documentation.

### Service Layer

Handles business logic and evaluation orchestration.

### Evaluation Engine

Calculates evaluation metrics and validation results.

### Semantic Similarity Engine

Uses Sentence Transformers to compare expected and actual outputs.

### Regression Detection

Identifies quality degradation between baseline and current model outputs.

### PostgreSQL

Stores evaluations, metrics, and validation history.
