# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import habits

app = FastAPI(title="Lattivo API")

origins = [
    "http://localhost:3000",
    "https://lattivo-frontend.vercel.app",  # replace with lattivo.com when rehosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(habits.router, prefix="/habits", tags=["habits"])


@app.get("/")
async def root():
    return {"message": "Tomato"}
