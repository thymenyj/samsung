from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import load_kaggle_data_to_database
from app.routers import train_random_forest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(load_kaggle_data_to_database.router)
app.include_router(train_random_forest.router)