from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.auth.core import CurrentUserDep

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/test-auth")
async def admin_test_auth(user: CurrentUserDep):
    return JSONResponse(content={"ok": True})


@router.get("/me")
async def get_me(user: CurrentUserDep):
    return user
