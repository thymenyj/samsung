from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def load_kaggle_data_to_database():
    try:
        pass
    except Exception:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


    return 
