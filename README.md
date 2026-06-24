# AI Regression Validation Framework

## Overview

AI Regression Validation Framework is an NLP-powered evaluation platform designed to validate and benchmark AI model outputs. The system combines traditional evaluation metrics with semantic similarity analysis to detect regressions and quality degradation across model versions.

## Features

* Evaluation lifecycle management
* Precision, Recall, and F1-score calculation
* Semantic similarity analysis using Sentence Transformers
* Automated regression detection
* PostgreSQL persistence layer
* RESTful FastAPI endpoints
* Docker containerization
* GitHub Actions CI/CD pipeline
* Automated testing with PyTest

## Technology Stack

### Backend

* FastAPI
* Python
* SQLAlchemy

### Database

* PostgreSQL

### AI / NLP

* Sentence Transformers
* Semantic Similarity Evaluation

### DevOps

* Docker
* GitHub Actions

### Testing

* PyTest

## System Workflow

1. Create evaluation requests.
2. Submit expected and actual model outputs.
3. Generate evaluation metrics.
4. Calculate semantic similarity scores.
5. Detect quality regressions.
6. Store results for future comparison.

## Running Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker build -t ai-regression-framework .
docker run -p 8000:8000 ai-regression-framework
```

## Testing

```bash
python -m pytest tests -v
```

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

## Future Enhancements

* Kubernetes deployment
* Model benchmarking dashboard
* Multi-model comparison workflows
* Automated evaluation scheduling
* Cloud deployment
