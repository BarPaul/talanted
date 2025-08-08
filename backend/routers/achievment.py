from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import APIKeyHeader
from passlib.hash import bcrypt
from config import SECRET_KEY
from models import UserRole
from database import get_db
import crud
import schemas.schemas as schemas

router = APIRouter(prefix="/teacher", tags=["teacher"])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь не авторизован",
)
oauth2 = APIKeyHeader(name="Authorization")
async def get_user(token: str = Depends(oauth2), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError or ExpiredSignatureError:
        raise credentials_exception
    user = await crud.get_user_by(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@router.get("/info")
async def info(child: schemas.ChildCreate, db: AsyncSession = Depends(get_db)):
    pass

@router.patch("/change")
async def change(child: schemas.ChildCreate, db: AsyncSession = Depends(get_db)):
    pass

@router.delete("/delete")
async def change(child: schemas.ChildCreate, db: AsyncSession = Depends(get_db)):
    pass