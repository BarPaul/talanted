from fastapi import APIRouter, Depends, Request, Response
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from passlib.hash import bcrypt
from config import SECRET_KEY
from database import get_db
import crud
import schemas
import exceptions

router = APIRouter(prefix="/auth", tags=["auth"])

async def get_user(request: Request, db: AsyncSession = Depends(get_db)) -> User | None:
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[-1]
    if not token:
        raise exceptions.CREDENTIALS
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise exceptions.CREDENTIALS
    except (JWTError, ExpiredSignatureError):
        raise exceptions.CREDENTIALS
    user = await crud.get_obj_by(db, User, email=email)
    if user is None:
        raise exceptions.CREDENTIALS
    if not user.is_active:
        raise exceptions.NOT_ACTIVE
    return user

@router.get("/me", response_model=schemas.UserResponse)
async def me(user: User = Depends(get_user)):
    return user.__dict__

@router.post("/register", 
    name="Регистрация", 
    description="Регистрация пользователя в системе",
    response_model=schemas.UserResponse
)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_obj_by(db, User, schemas.UserResponse, email=user.email)
    if existing:
        raise exceptions.EMAIL
    new_user = await crud.create_user(db, 
        email=user.email, 
        hashed_password=bcrypt.hash(user.password),
        name=user.name,
        role=user.role,
        city=user.city,
    )
    return schemas.UserResponse.model_validate(new_user)

@router.post("/activate-user", response_model=schemas.UserResponse)
async def activate_user(
    data: schemas.UserActivate,
    db: AsyncSession = Depends(get_db), 
    admin: User = Depends(get_user)
):
    user = await crud.get_obj_by(db, User, email=data.email)
    if not user:
        raise exceptions.NOT_EXISTS
    if admin.role.level <= 1 or admin.role.level == 2 and admin.city != user.city:
        raise exceptions.NOT_ALLOWED
    if user.is_active:
        raise exceptions.ALREADY_ACTIVATED
    user = await crud.activate_user(db, user)
    return schemas.UserResponse.model_validate(user)

@router.post("/login", response_model=schemas.TokenResponse)
async def login(
    response: Response,
    data: schemas.UserLogin, 
    db: AsyncSession = Depends(get_db)
):
    user = await crud.get_obj_by(db, User, schemas.UserResponse, email=data.email)
    if not user:
        raise exceptions.NOT_EXISTS
    if not user.is_active:
        raise exceptions.NOT_ACTIVE
    if not bcrypt.verify(data.password, user.hashed_password):
        raise exceptions.WRONG_PASSWORD
    token_data = {
        "sub": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        secure=False,
        samesite="Lax"
    )
    
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout", response_model=schemas.OkResponse)
async def logout(response: Response, _ = Depends(get_user)):
    response.delete_cookie("access_token")
    return {"ok": True}

@router.patch("/change-password", response_model=schemas.UserResponse)
async def change_password(data: schemas.PasswordChange, db: AsyncSession = Depends(get_db)):
    user = await crud.get_obj_by(db, User, schemas.UserResponse, email=data.email)
    if not user:
        raise exceptions.NOT_EXISTS
    if not bcrypt.verify(data.old_password, user.hashed_password):
        raise exceptions.WRONG_PASSWORD
    await crud.update_user_password(db, user, bcrypt.hash(data.new_password))
    return schemas.UserResponse.model_validate(user)

@router.delete("/delete", response_model=schemas.OkResponse)
async def delete_user(
    user: schemas.UserDelete,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_user)
):
    if user.id == current_user.id:
        raise exceptions.SELF_DELETING
    user_to_delete = await crud.get_obj_by(db, User, schemas.UserResponse, id=user.id)
    if not user_to_delete:
        raise exceptions.NOT_EXISTS
    if user_to_delete.role.level <= current_user.role.level:
        raise exceptions.NOT_ALLOWED
    await crud.delete_user(db, user_to_delete)
    return {"ok": True}
