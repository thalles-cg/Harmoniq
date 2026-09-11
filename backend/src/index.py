from fastapi import FastAPI
from src.router import router

app = FastAPI(
  title="Harmoniq API",
  description="API do sistema Harmoniq.",
  version="0.1.0",
)

app.include_router(router)