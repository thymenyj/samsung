import os
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi import APIRouter, HTTPException

from app.src.data_processors.DataProcessor import DataProcessor
from app.src.databases.AnalyticsDatabase import AnalyticsDatabase

router = APIRouter()


@router.post("/load_kaggle_data_to_database")
async def load_kaggle_data_to_database():
    try:
        connection_string = os.getenv("ANALYTICS_DATABASE_CONNECTION_STRING")
        analytics_database = AnalyticsDatabase(connection_string)
        
        data_processor = DataProcessor(analytics_database)
        data_processor.process()

        
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR) from exc

    return 
