from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_user
from database import get_db
from models import User, Teacher
import crud
import schemas
import exceptions

router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.get("/all", response_model=schemas.TeachersResponse)
async def all_teachers(
    data: schemas.GetAll = Depends(),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    if not data.id or user.role.level <= 1:
        data.id = user.id
    teachers = await crud.get_obj_by(
        db, Teacher, schemas.TeacherResponse, need_all=True, 
        load_relationships=[Teacher.school], school_id=data.id
    )
    return schemas.TeachersResponse.model_validate(schemas.TeachersResponse(teachers=teachers))

@router.post("/create", response_model=schemas.TeacherResponse)
async def create_teacher(
    teacher: schemas.TeacherCreate, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    teacher = await crud.create_teacher(db, teacher.name, user)
    return schemas.TeacherResponse.model_validate(teacher)

@router.patch("/change", response_model=schemas.TeacherResponse)
async def change_teacher(
    teacher: schemas.TeacherChange, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    prev_teacher = await crud.get_obj_by(
        db, Teacher,
        load_relationships=[Teacher.school],
        id=teacher.id, school_id=user.id
    )
    if not prev_teacher:
        raise exceptions.TEACHER_NOT_EXISTS
    if teacher.school_id != user.id and user.role.level <= 1 or \
        user.role.level == 2 and teacher.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    updated_teacher = await crud.update_teacher(db, prev_teacher, teacher.new_name)
    return schemas.TeacherResponse.model_validate(updated_teacher)

@router.delete("/delete", response_model=schemas.OkResponse)
async def delete_teacher(
    teacher: schemas.GradeDelete, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    teacher = await crud.get_obj_by(
        db, Teacher, 
        load_relationships=[teacher.school],
        id=teacher.id, school_id=user.id if user.role.level <= 1 else None
    )
    if not teacher:
        raise exceptions.TEACHER_NOT_EXISTS
    if user.role.level == 2 and teacher.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    await crud.delete_teacher(db, teacher)
    return {"ok": True}

@router.get("/{teacher_id}", response_model=schemas.TeacherResponse)
async def info_teacher(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    teacher = await crud.get_obj_by(
        db, Teacher, load_relationships=[Teacher.school], 
        school_id=user.id if user.role.level <= 1 else None, id=teacher_id
    )
    if not teacher:
        raise exceptions.TEACHER_NOT_EXISTS
    if user.role.level == 2 and teacher.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    return schemas.TeacherResponse.model_validate(teacher)
