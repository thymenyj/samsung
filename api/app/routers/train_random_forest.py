import os
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi import APIRouter, HTTPException

from app.src.model_trainers.RandomForestTrainer import RandomForestTrainer
from app.src.databases.AnalyticsDatabase import AnalyticsDatabase

router = APIRouter()


@router.get("/train_random_forest")
async def train_random_forest():
    try:
        connection_string = os.getenv("ANALYTICS_DATABASE_CONNECTION_STRING")
        analytics_database = AnalyticsDatabase(connection_string)
        
        data_processor = RandomForestTrainer(analytics_database)
        data_processor.train()

        
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR) from exc

    return 
