from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_user
from database import get_db
from models import User, Child, Grade
import crud
import schemas
import exceptions

router = APIRouter(prefix="/child", tags=["child"])

@router.get("/all/{grade_id}", response_model=schemas.ChildsResponse)
async def all_childs(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    grade = await crud.get_obj_by(
        db, Grade, id=grade_id,
        load_relationships=[Grade.school]
    )
    if not grade:
        raise exceptions.GRADE_NOT_EXISTS
    if grade.school.id != user.id and user.role.level <= 1:
        raise exceptions.NOT_ALLOWED
    childs = await crud.get_obj_by(
        db, Child, schemas.ChildResponse, need_all=True, 
        load_relationships=[Child.grade], grade_id=grade_id
    )
    return schemas.ChildsResponse.model_validate(schemas.ChildsResponse(childs=childs))

@router.post("/create", response_model=schemas.ChildResponse)
async def create_child(
    child: schemas.ChildCreate, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    grade = await crud.get_obj_by(
        db, Grade, load_relationships=[Grade.school],
        id=child.grade_id, school_id=user.id
    )
    if not grade:
        raise exceptions.GRADE_NOT_EXISTS
    child = await crud.create_child(db, child.name, grade)
    return schemas.ChildResponse.model_validate(child)

@router.patch("/change", response_model=schemas.ChildResponse)
async def change_child(
    child: schemas.ChildChange, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    prev_child = await crud.get_obj_by(
        db, Child, id=child.id,
        load_relationships=[Child.grade, Child.grade.school]
    )
    if not prev_child:
        raise exceptions.CHILD_NOT_EXISTS
    new_grade = await crud.get_obj_by(
        db, Grade, 
        load_relationships=[Grade.school, Grade.children],
        id=prev_child.new_grade_id, school_id=prev_child.grade.school_id
    )
    if not new_grade:
        raise exceptions.GRADE_NOT_EXISTS
    if prev_child.grade.school.id != user.id and user.role.level <= 1 or \
        user.role.level == 2 and prev_child.grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    updated_child = await crud.update_child(db, prev_child, child.new_name, new_grade)
    return schemas.ChildResponse.model_validate(updated_child)

@router.delete("/delete", response_model=schemas.OkResponse)
async def delete_child(
    child: schemas.GradeDelete, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    child = await crud.get_obj_by(
        db, Child, 
        load_relationships=[Child.grade, Child.grade.school],
        id=child.id
    )
    if not child:
        raise exceptions.GRADE_NOT_EXISTS
    if child.grade.school.id != user.id \
    or user.role.level == 2 and child.grade.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    await crud.delete_child(db, child)
    return {"ok": True}


@router.get("/{child_id}", response_model=schemas.ChildResponse)
async def info_child(
    child_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_user)
):
    child = await crud.get_obj_by(
        db, Child, load_relationships=[Child.grade, Child.grade.school], 
        grade_id=user.id if user.role.level <= 1 else None, id=child_id
    )
    if not child:
        raise exceptions.CHILD_NOT_EXISTS
    if user.role.level == 2 and child.school.city != user.city:
        raise exceptions.NOT_ALLOWED
    return schemas.ChildResponse.model_validate(child)
