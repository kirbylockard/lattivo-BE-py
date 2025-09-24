from fastapi import FastAPI

from app.api import habits

app = FastAPI()
app.include_router(habits.router)
