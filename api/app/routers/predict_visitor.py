from logging import error, info
from pickle import load
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi import APIRouter, HTTPException

from app.data_models.Visitor import Visitor

router = APIRouter()


@router.post("/predict_visitor")
async def predict_visitor(visitor: Visitor):
    try:
        random_forest = load(open("/app/ml_models/random_forest.pkl", 'rb'))

        predictions = random_forest.predict([visitor.features])

        actual = visitor.revenue_positive
        
        info("Predicted visitor successfully!")
        return {
            "predictions": list(predictions),
            "actual": [actual]
        }

    except Exception as exc:
        error(f"Failed to predict visitor. --> {exc}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR) from exc
