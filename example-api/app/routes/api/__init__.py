from fastapi import APIRouter

from . import auth, utils

router = APIRouter(prefix="/api", tags=["API"])
router.include_router(utils.router)
router.include_router(auth.router)
