from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.dependencies.db import SessionDep
from app.models.users import User

router = APIRouter(prefix="/auth")

exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
)


@router.post("/token")
async def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    if user := session.exec(
        select(User).where(User.email == form_data.username)
    ).first():
        return JSONResponse(
            content={"access_token": user.email, "token_type": "bearer"}
        )
    else:
        raise exception
