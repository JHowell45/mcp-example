from fastapi import APIRouter

from . import films

router = APIRouter(prefix="/v1", tags=["V1"])
router.include_router(films.router)
