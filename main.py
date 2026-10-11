from fastapi import FastAPI

from routers.items import router as items_router


app = FastAPI(
    title="Simot API",
    description="A backend for managing household pantry inventory.",
    version="0.1.0",
)

app.include_router(items_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}