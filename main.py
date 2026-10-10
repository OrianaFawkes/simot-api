
from fastapi import FastAPI

app = FastAPI(
    title="Simot API",
    description="A backend for managing household pantry inventory.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}