from models import User, UserCity, UserRole, Child, Grade, Teacher, Achievement, AchieveLevel, AchieveType, AchieveTeam, AchieveFormat, AchievePlace
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, literal_column, text
from sqlalchemy.orm import aliased
from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_db
from typing import List, Optional
from pydantic import BaseModel, Field

router = APIRouter(prefix="/stats", tags=["stats"])

class SchoolRatingItem(BaseModel):
    school_id: int
    name: str
    city: UserCity
    total_ratio: float
    place: int

class MunicipalityRatingItem(BaseModel):
    city: UserCity
    total_ratio: float
    place: int
    schools: List[SchoolRatingItem] = Field(default_factory=list)

class MunicipalityRatingsResponse(BaseModel):
    municipalities: List[MunicipalityRatingItem]

@router.get("/counts")
async def get_counts(
    db: AsyncSession = Depends(get_db),
):
    child_result = await db.execute(select(Child))
    children = child_result.scalars().all()
    
    teacher_result = await db.execute(select(Teacher))
    teachers = teacher_result.scalars().all()
    
    achievements_result = await db.execute(select(Achievement))
    achievements = achievements_result.scalars().all()
    
    return {
        "child": len(children),
        "teacher": len(teachers),
        "achievements": len(achievements)
    }

@router.get("/ratings/municipalities", response_model=MunicipalityRatingsResponse)
async def get_municipalities_rating(
    city: Optional[UserCity] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        municipalities = list(UserCity) if not city else [city]
        child_alias = aliased(Child)
        achievement_alias = aliased(Achievement)
        ratio_expr = (
            case(
                (achievement_alias.type == AchieveType.SCIENCE, 1.4),
                (achievement_alias.type == AchieveType.ART, 1.4),
                (achievement_alias.type == AchieveType.SPORT, 1.4),
                else_=1.4
            ) *
            case(
                (achievement_alias.level == AchieveLevel.MUN, 1.25),
                (achievement_alias.level == AchieveLevel.INTER_MUN, 1.5),
                (achievement_alias.level == AchieveLevel.REGION, 2.25),
                (achievement_alias.level == AchieveLevel.INTER_REG, 3.75),
                (achievement_alias.level == AchieveLevel.ALL_RUS, 4.5),
                else_=1.25
            ) *
            case(
                (achievement_alias.format == AchieveFormat.REMOTE, 0.5),
                (achievement_alias.format == AchieveFormat.OWN, 1.5),
                else_=0.5
            ) *
            case(
                (achievement_alias.team == AchieveTeam.SOLO, 1.75),
                (achievement_alias.team == AchieveTeam.TEAM, 1.25),
                else_=1.25
            ) *
            case(
                (achievement_alias.place == AchievePlace.GRAN, 1.3),
                (achievement_alias.place == AchievePlace.FIRST, 1.25),
                (achievement_alias.place == AchievePlace.SECOND, 0.75),
                (achievement_alias.place == AchievePlace.THIRD, 0.5),
                (achievement_alias.place == AchievePlace.PARTICLANT, 0.25),
                else_=0.25
            )
        )
        
        date_ratio_expr = case(
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 1095"), 0.0),
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 730"), 0.25),
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 365"), 0.75),
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 30"), 1.25),
            else_=1.5
        )
        
        total_ratio_expr = ratio_expr * date_ratio_expr
        
        municipalities_data = []
        
        for city in municipalities:
            schools_query = (
                select(
                    User.id,
                    User.name,
                    User.city,
                    func.sum(total_ratio_expr).label("total_ratio")
                )
                .join(Grade, Grade.school_id == User.id)
                .join(child_alias, child_alias.grade_id == Grade.id)
                .join(achievement_alias, achievement_alias.child_id == child_alias.id)
                .filter(User.role == UserRole.SCHOOL)
                .filter(User.city == city)
                .group_by(User.id, User.name, User.city)
                .order_by(func.sum(total_ratio_expr).desc())
            )
            
            schools_result = await db.execute(schools_query)
            school_ratings = schools_result.all()
            
            schools = []
            for index, (school_id, name, city, total_ratio) in enumerate(school_ratings, 1):
                schools.append({
                    "school_id": school_id,
                    "name": name,
                    "city": city,
                    "total_ratio": float(total_ratio) if total_ratio else 0.0,
                    "place": index
                })
            
            city_schools_query = select(User).filter(
                User.role == UserRole.SCHOOL,
                User.city == city
            )
            city_schools_result = await db.execute(city_schools_query)
            city_schools = city_schools_result.scalars().all()
            
            existing_school_ids = [school["school_id"] for school in schools]
            
            for school in city_schools:
                if school.id not in existing_school_ids:
                    schools.append({
                        "school_id": school.id,
                        "name": school.name,
                        "city": school.city,
                        "total_ratio": 0.0,
                        "place": len(schools) + 1
                    })
            
            schools.sort(key=lambda x: x["total_ratio"], reverse=True)
            
            for index, school in enumerate(schools, 1):
                school["place"] = index
            
            total_municipality_ratio = sum(school["total_ratio"] for school in schools)
            
            municipalities_data.append({
                "city": city,
                "total_ratio": total_municipality_ratio,
                "schools": schools
            })
        municipalities_data.sort(key=lambda x: x["total_ratio"], reverse=True)
        for index, municipality in enumerate(municipalities_data, 1):
            municipality["place"] = index
            
        response = {
            "municipalities": municipalities_data
        }
        return response

    except Exception as e:
        print(f"Error in municipalities rating: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при получении рейтинга муниципалитетов")
