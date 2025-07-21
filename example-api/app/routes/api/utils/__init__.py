from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/utils")


@router.get("/health-check")
async def health_check() -> JSONResponse:
    return JSONResponse(content={"ok": True})
