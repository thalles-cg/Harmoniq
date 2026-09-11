from fastapi import FastAPI

app = FastAPI(
  title="Harmoniq API",
  description="API do sistema Harmoniq.",
  version="0.1.0",
)

@app.get("/health")
def health():
  return {"status": "ok"}