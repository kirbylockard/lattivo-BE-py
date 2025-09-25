from fastapi import FastAPI
from app.api import habits  # import the router

app = FastAPI()

# Include the habits routes
app.include_router(habits.router, prefix="/habits", tags=["habits"])

@app.get("/")
async def root():
    return {"message": "Tomato"}
