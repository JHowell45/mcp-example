from app import routes
from fastapi import FastAPI

app = FastAPI(title="Example API for MCP")
app.include_router(routes.router)
