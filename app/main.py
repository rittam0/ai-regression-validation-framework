from fastapi import FastAPI
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

app = FastAPI()


ground_truth = [
    1, 1, 1, 0, 0,
    1, 0, 1, 0, 1
]

predictions = [
    1, 1, 0, 0, 0,
    1, 1, 1, 0, 1
]


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():

    precision = precision_score(
        ground_truth,
        predictions
    )

    recall = recall_score(
        ground_truth,
        predictions
    )

    f1 = f1_score(
        ground_truth,
        predictions
    )

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1, 3)
    }
