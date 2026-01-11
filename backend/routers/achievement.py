from models import User, UserCity, Child, Grade, Teacher, Achievement, \
    AchieveFormat, AchievePlace, AchieveLevel, AchieveTeam, AchieveType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import APIRouter, Depends, Form, File, UploadFile, Query
from os import path, remove
from database import get_db
from .auth import get_user
from typing import List, Optional
import exceptions
import schemas
import crud

router = APIRouter(prefix="/achievement", tags=["achievement"])

@router.get("/all", response_model=List[schemas.AchievementResponse])
async def all_achievements(
    db: AsyncSession = Depends(get_db),
    city: Optional[str] = Query(None, description="Фильтр по муниципалитету (городу)"),
    achieve_type: Optional[str] = Query(None, description="Фильтр по направлению (Наука, Искусство, Спорт)"),
    child_id: Optional[int] = Query(None, description="Фильтр по ID ребенка"),
    name: Optional[str] = Query(None, description="Фильтр по названию достижения")
):
    query = select(Achievement).options(
        selectinload(Achievement.child),
        selectinload(Achievement.teacher)
    )

    if achieve_type:
        try:
            achieve_type_enum = AchieveType(achieve_type)
            query = query.filter(Achievement.type == achieve_type_enum)
        except ValueError:
            raise exceptions.WRONG_TYPE

    if child_id:
        query = query.filter(Achievement.child_id == child_id)

    if name:
        query = query.filter(Achievement.name.ilike(f"%{name}%"))

    if city:
        try:
            city_enum = UserCity(city)
            query = query.join(Achievement.child).join(Child.grade).join(Grade.school).filter(User.city == city_enum)
        except ValueError:
            raise exceptions.WRONG_CITY

    result = await db.execute(query)
    achievements = result.scalars().all()

    return achievements

@router.get("/all/{child_id}", response_model=List[schemas.AchievementResponse])
async def all_child_achievements(
    child_id: int,
    db: AsyncSession = Depends(get_db),
):
    child = await crud.get_obj_by(db, Child, id=child_id, 
        load_relationships=[Child.grade, selectinload(Child.grade).selectinload(Grade.school)]
    )
    if not child:
        raise exceptions.CHILD_NOT_EXISTS
    achievements = await crud.get_obj_by(
        db, Achievement, need_all=True,
        child_id=child_id,
        load_relationships=[Achievement.child, Achievement.teacher]
    )
    return achievements

@router.get("/{achievement_id}", response_model=schemas.AchievementResponse)
async def get_achievement(
    achievement_id: int,
    db: AsyncSession = Depends(get_db),
):
    achievement = await crud.get_obj_by(
        db, Achievement,
        id=achievement_id,
        load_relationships=[
            Achievement.child, 
            Achievement.teacher,
            selectinload(Achievement.child).selectinload(Child.grade),
            selectinload(Achievement.child).selectinload(Child.grade).selectinload(Grade.school)
        ]
    )
    if not achievement:
        raise exceptions.ACHIEVEMENT_NOT_EXISTS
    return schemas.AchievementResponse.model_validate(achievement)

@router.post("/create", response_model=schemas.AchievementResponse)
async def create_achievement(
    name: str = Form(...),
    type: AchieveType = Form(...),
    team: AchieveTeam = Form(...),
    level: AchieveLevel = Form(...),
    format: AchieveFormat = Form(...),
    place: AchievePlace = Form(...),
    date_str: str = Form(..., description="В формате ДД.ММ.ГГГГ", example="01.05.2025"),
    child_id: int = Form(...),
    teacher_id: int = Form(...),
    file: UploadFile = File(),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    is_success, date = crud.validate_date(date_str)
    if not is_success:
        raise date
    child = await crud.get_obj_by(db, Child,
        id=child_id, 
        load_relationships=[selectinload(Child.grade)]
    )
    if not child:
        raise exceptions.CHILD_NOT_EXISTS
    if user.role.level <= 1 and child.grade.school.id != user.id:
        raise exceptions.NOT_ALLOWED
    elif user.role.level == 2 and child.grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    teacher = await crud.get_obj_by(db, Teacher, id=teacher_id)
    if not teacher:
        raise exceptions.TEACHER_NOT_EXISTS
    file_path = await crud.save_achievement_file(file)
    achievement = Achievement(
        file_path=file_path, name=name, type=type, team=team,
        level=level, format=format, place=place,
        date=date, child=child, teacher=teacher
    )
    achievement = await crud.create_achievement(db, achievement)
    return schemas.AchievementResponse.model_validate(achievement)

@router.patch("/change", response_model=schemas.AchievementResponse)
async def change_achievement(
    achievement_id: int = Form(...),
    name: str = Form(...),
    type: AchieveType = Form(...),
    team: AchieveTeam = Form(...),
    level: AchieveLevel = Form(...),
    format: AchieveFormat = Form(...),
    place: AchievePlace = Form(...),
    date_str: str = Form(..., description="В формате ДД.ММ.ГГГГ", example="01.05.2025"),
    file: UploadFile = File(),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    is_success, date = crud.validate_date(date_str)
    if not is_success:
        raise date
    achievement = await crud.get_obj_by(
        db, Achievement,
        id=achievement_id,
        load_relationships=[
            selectinload(Achievement.child).selectinload(Child.grade).selectinload(Grade.school)
        ]
    )
    if not achievement:
        raise exceptions.ACHIEVEMENT_NOT_EXISTS
    if user.role.level <= 1 and achievement.child.grade.school.id != user.id:
        raise exceptions.NOT_ALLOWED
    elif user.role.level == 2 and achievement.child.grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    achievement = await crud.update_achievement(db, achievement,
        name, type, level, format, 
        team, place, date, file
    )
    return schemas.AchievementResponse.model_validate(achievement)

@router.delete("/delete", response_model=schemas.OkResponse)
async def delete_achievement(
    data: schemas.AchievementDelete,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    achievement = await crud.get_obj_by(
        db, Achievement,
        id=data.id,
        load_relationships=[
            selectinload(Achievement.child).selectinload(Child.grade).selectinload(Grade.school)
        ]
    )
    if not achievement:
        raise exceptions.ACHIEVEMENT_NOT_EXISTS
    if user.role.level <= 1 and achievement.child.grade.school.id != user.id:
        raise exceptions.NOT_ALLOWED
    elif user.role.level == 2 and achievement.child.grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    if path.exists(achievement.file_path):
        remove(achievement.file_path)
    await crud.delete_achievement(db, achievement)
    return {"ok": True}
