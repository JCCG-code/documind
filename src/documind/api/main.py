from fastapi import FastAPI

from documind.api.routes.documents import router as documents_router

# Fast API initialization
app = FastAPI(title="DocuMind", version="0.1.0")


# My routes
app.include_router(documents_router)


# General routes
@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
