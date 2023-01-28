from fastapi import FastAPI
from .routers import predictions_router

app = FastAPI()
app.include_router(predictions_router, prefix="/prediction", tags=["predictions"])