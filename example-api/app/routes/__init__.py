from fastapi import APIRouter

from . import admin, api

router = APIRouter()
router.include_router(admin.router)
router.include_router(api.router)
