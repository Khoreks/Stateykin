from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from schemas.user import UserCreate
from schemas.response import BaseResponse
from database.session import get_database
from services.crud.user import create_new_user

router = APIRouter()


@router.post("/signup", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_database)):
    if create_new_user(user=user, db=db):
        return {
            "success": True,
            "message": "Регистрация прошла успешно",
            "value": True
        }
    raise HTTPException(409, detail="Пользователь уже зарегистрирован")
