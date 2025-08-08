from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_user
from database import get_db
from models import User, Grade
import crud
import schemas
import exceptions

router = APIRouter(prefix="/grade", tags=["grade"])

@router.get("/all", response_model=schemas.GradesResponse)
async def all_grades(
    data: schemas.GetAll = Depends(),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    if not data.id or user.role.level <= 1:
        data.id = user.id
    grades = await crud.get_obj_by(
        db, Grade, schemas.GradeResponse, need_all=True, 
        load_relationships=[Grade.children], school_id=data.id
    )
    return schemas.GradesResponse.model_validate(schemas.GradesResponse(grades=grades))

@router.post("/create", response_model=schemas.GradeResponse)
async def create_grade(
    grade: schemas.GradeCreate, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    grade = await crud.create_grade(db, grade.grade, grade.parallel, user)
    return schemas.GradeResponse.model_validate(grade)

@router.patch("/change", response_model=schemas.GradeResponse)
async def change_grade(
    grade: schemas.GradeChange, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    prev_grade = await crud.get_obj_by(
        db, Grade,
        load_relationships=[Grade.children, Grade.school],
        id=grade.id, school_id=user.id
    )
    if not prev_grade:
        raise exceptions.GRADE_NOT_EXISTS
    if prev_grade.school_id != user.id and user.role.level <= 1 or \
        user.role.level == 2 and grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    updated_grade = await crud.update_grade(db, prev_grade, grade.new_grade, grade.new_parallel)
    return schemas.GradeResponse.model_validate(updated_grade)

@router.delete("/delete", response_model=schemas.OkResponse)
async def delete_grade(
    grade: schemas.GradeDelete, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    grade = await crud.get_obj_by(
        db, Grade, 
        load_relationships=[Grade.children, Grade.school],
        id=grade.id, school_id=user.id if user.role.level <= 1 else None
    )
    if not grade:
        raise exceptions.GRADE_NOT_EXISTS
    if user.role.level == 2 and grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    await crud.delete_grade(db, grade)
    return {"ok": True}

@router.get("/{grade_id}", response_model=schemas.GradeResponse)
async def info_grade(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    grade = await crud.get_obj_by(
        db, Grade, load_relationships=[Grade.children, Grade.school], 
        school_id=user.id if user.role.level <= 1 else None, id=grade_id
    )
    if not grade:
        raise exceptions.GRADE_NOT_EXISTS
    if user.role.level == 2 and grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    return schemas.GradeResponse.model_validate(grade)
