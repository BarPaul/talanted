from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload, strategy_options
from models import User, UserRole, UserCity, Child, Grade, Teacher, Achievement, \
    AchieveFormat, AchievePlace, AchieveTeam, AchieveLevel, AchieveType
from schemas import UserResponse, GradeResponse, ChildResponse, TeacherResponse, AchievementResponse
from datetime import datetime
from config import ALLOWED_EXTENSIONS
from uuid import uuid4
from fastapi import UploadFile
from os import path, makedirs, remove
import exceptions

def validate_date(date_str: str):
    print(date_str)
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        return False, exceptions.WRONG_DATEFORMAT
    now = datetime.today().date()
    if date > now:
        return False, exceptions.IN_FUTURE
    if date <= now - timedelta(days=3 * 365):
        return False, exceptions.TOO_OLDDATE
    return True, date

async def save_achievement_file(file: UploadFile) -> str:
    ext = path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise exceptions.WRONG_EXTENSION
    unique_filename = f"{uuid4()}{ext}"
    save_path = path.join("achievements", unique_filename)
    makedirs(path.dirname(save_path), exist_ok=True)
    content = await file.read()
    with open(save_path, "wb") as buffer:
        buffer.write(content)
    return save_path

async def get_obj_by(db: AsyncSession, Class, Response=None, need_all=False, load_relationships: list = None, **kwargs):
    kwargs = dict(filter(lambda item: item[-1] is not None, kwargs.items()))
    query = select(Class).filter_by(**kwargs)
    if load_relationships:
        for relation in load_relationships:
            query = query.options(relation if isinstance(relation, strategy_options._AbstractLoad) else selectinload(relation))
    result = await db.execute(query)
    if need_all:
        orm_objs = result.scalars().all()
        if not orm_objs:
            return []
        return [Response.model_validate(obj) for obj in orm_objs] if Response else orm_objs
    orm_obj = result.scalar_one_or_none()
    if not orm_obj:
        return None
    return Response.model_validate(orm_obj) if Response else orm_obj

async def create_user(
    db: AsyncSession, 
    email: str, 
    hashed_password: str, 
    name: str,
    role: UserRole,
    city: UserCity,
    is_active: bool = False
):
    user = User(
        email=email, 
        hashed_password=hashed_password,
        name=name,
        role=role,
        city=city,
        is_active=is_active
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)

async def activate_user(db: AsyncSession, user: User):
    user.is_active = True
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)

async def update_user_password(db: AsyncSession, user: User, new_hash: str):
    user.hashed_password = new_hash
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)

async def delete_user(db: AsyncSession, user: User):
    await db.execute(delete(User).where(User.id == user.id))
    await db.commit()

# GRADE

async def create_grade(db: AsyncSession, grade: int, parallel: str, school: User):
    grade_obj = Grade(
        grade=grade, parallel=parallel, 
        school=school, school_id=school.id, 
        children=[]
    )
    db.add(grade_obj)
    await db.commit()
    await db.refresh(grade_obj, ["children", "school"])
    return GradeResponse.model_validate(grade_obj)

async def update_grade(db: AsyncSession, grade: Grade, new_grade: int, new_parallel: str):
    grade.grade = new_grade
    grade.parallel = new_parallel
    await db.commit()
    await db.refresh(grade, ["children", "school"])
    return GradeResponse.model_validate(grade)

async def delete_grade(db: AsyncSession, grade: Grade):
    await db.execute(delete(Grade).where(Grade.id == grade.id))
    await db.commit()

# CHILD

async def create_child(db: AsyncSession, name: str, grade: Grade):
    child = Child(name=name, grade=grade)
    db.add(child)
    await db.commit()
    await db.refresh(child)
    return ChildResponse.model_validate(child)

async def update_child(db: AsyncSession, child: Child, name: str, grade: Grade):
    child.name = name
    child.grade = grade
    db.add(child)
    await db.commit()
    await db.refresh(child)
    return await get_obj_by(db, Child, ChildResponse, child.id)

async def delete_child(db: AsyncSession, child: Child):
    await db.execute(delete(Child).where(Child.id == child.id))
    await db.commit()

# TEACHER

async def create_teacher(db: AsyncSession, name: str, school: User):
    teacher = Teacher(name=name, school=school)
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)
    return TeacherResponse.model_validate(teacher)

async def update_teacher(db: AsyncSession, teacher: Teacher, name: str):
    teacher.name = name
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)
    return TeacherResponse.model_validate(teacher)

async def delete_teacher(db: AsyncSession, teacher: Teacher):
    stmt = delete(Teacher).where(Teacher.id == teacher.id)
    await db.execute(stmt)
    await db.commit()

# ACHIEVEMENT
async def create_achievement(db: AsyncSession, achievement: Achievement):
    db.add(achievement)
    await db.commit()
    await db.refresh(achievement)
    return achievement

async def update_achievement(db: AsyncSession, 
    achievement: Achievement, 
    name: str,
    type: AchieveType,
    level: AchieveLevel,
    format: AchieveFormat,
    team: AchieveTeam,
    place: AchievePlace,
    date: datetime.date,
    file: UploadFile, 
):
    achievement.name = name
    achievement.type = type
    achievement.level = level
    achievement.format = format
    achievement.team = team
    achievement.place = place
    achievement.date = date
    if path.exists(achievement.file_path):
        remove(achievement.file_path)
    achievement.file_path = await save_achievement_file(file)
    db.add(achievement)
    await db.commit()
    await db.refresh(achievement)
    return AchievementResponse.model_validate(achievement)

async def delete_achievement(db: AsyncSession, achievement: Achievement):
    stmt = delete(Achievement).where(Achievement.id == achievement.id)
    await db.execute(stmt)
    await db.commit()

