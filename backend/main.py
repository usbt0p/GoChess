# backend/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Go-Chess Backend is running!"}

# Placeholder for game routes
# Example:
# from src.infrastructure.api.game_routes import router as game_router
# app.include_router(game_router, prefix="/api/v1")
