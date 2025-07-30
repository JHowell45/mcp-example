from contextlib import asynccontextmanager

from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

from app import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    SentenceTransformer("all-MiniLM-L6-v2")
    yield


app = FastAPI(title="Example API for MCP", lifespan=lifespan)
app.include_router(routes.router)
