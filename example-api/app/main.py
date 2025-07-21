from fastapi import FastAPI

from app import routes

app = FastAPI(title="FastAPI Template")
app.include_router(routes.router)
