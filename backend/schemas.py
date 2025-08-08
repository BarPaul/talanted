from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from models import UserRole, UserCity
from typing import Annotated

# AUTH

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    city: UserCity
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserActivate(BaseModel):
    email: EmailStr

class UserDelete(BaseModel):
    id: int

class PasswordChange(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    name: str
    role: UserRole
    city: UserCity
    is_active: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class OkResponse(BaseModel):
    ok: bool = Field(default=True)

class GetAll(BaseModel):
    id: Annotated[int | None, Query(title="Айди")] = Field(default=None)

# GRADE

class GradeBase(BaseModel):
    grade: int = Field(..., ge=1, le=11)
    parallel: str = Field(..., max_length=1)

class GradeCreate(GradeBase):
    pass

class GradeResponse(GradeBase):
    id: int
    school_id: int
    children: list["ChildResponse"] = Field(default=[])
    
    class Config:
        from_attributes = True

class GradesResponse(BaseModel):
    grades: list[GradeResponse]

class GradeChange(BaseModel):
    id: int
    new_grade: int | None = Field(None, ge=1, le=11)
    new_parallel: str | None = Field(None, max_length=1)

class GradeDelete(BaseModel):
    id: int

# CHILD

class ChildBase(BaseModel):
    name: str
    grade_id: int

class ChildCreate(ChildBase):
    pass

class ChildResponse(ChildBase):
    id: int
    
    class Config:
        from_attributes = True

class ChildChange(BaseModel):
    id: int
    new_name: str | None = None
    new_grade_id: int | None = None

class ChildDelete(BaseModel):
    id: int

class ChildsResponse(BaseModel):
    childs: list[ChildResponse]

# TEACHER

class TeacherBase(BaseModel):
    name: str

class TeacherCreate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: int
    school_id: int
    
    class Config:
        from_attributes = True

class TeachersResponse(BaseModel):
    teachers: list[TeacherResponse] = []

class TeacherChange(BaseModel):
    id: int
    new_name: str | None = None
    new_school_id: int | None = None

class TeacherDelete(BaseModel):
    id: int

# GradeResponse.update_forward_refs()