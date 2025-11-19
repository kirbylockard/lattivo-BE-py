# app/main.py
from fastapi import FastAPI

from app.api import habits

app = FastAPI(title="Lattivo API")

app.include_router(habits.router, prefix="/habits", tags=["habits"])


@app.get("/")
async def root():
    return {"message": "Tomato"}
