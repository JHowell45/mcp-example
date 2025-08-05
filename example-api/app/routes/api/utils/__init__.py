from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/utils", tags=["utility"])


@router.get("/health-check")
async def health_check() -> JSONResponse:
    return JSONResponse(content={"ok": True})
