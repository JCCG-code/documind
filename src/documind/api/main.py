from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from documind.api.routes.documents import router as documents_router
from documind.api.routes.query import router as query_router
from documind.api.routes.search import router as search_router

# Fast API initialization
app = FastAPI(title="DocuMind", version="0.1.0")

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# My routes
app.include_router(documents_router)
app.include_router(search_router)
app.include_router(query_router)


# General routes
@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
