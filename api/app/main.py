from fastapi import FastAPI
from app.routers import load_kaggle_data_to_database

app = FastAPI()

app.include_router(load_kaggle_data_to_database.router)