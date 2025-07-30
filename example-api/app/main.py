from fastapi import FastAPI

from app import routes

app = FastAPI(title="Example API for MCP")
app.include_router(routes.router)
