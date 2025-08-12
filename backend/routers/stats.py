from models import User, UserCity, UserRole, Child, Grade, Teacher, Achievement, AchieveLevel, AchieveType, AchieveTeam, AchieveFormat, AchievePlace
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, literal_column, text
from sqlalchemy.orm import aliased
from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_db
from .auth import get_user
from typing import List, Optional
from pydantic import BaseModel, Field
import datetime

router = APIRouter(prefix="/stats", tags=["stats"])

# Схемы Pydantic для рейтингов
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
    """
    Получить количество записей в основных таблицах
    """
    # Получаем количество детей
    child_result = await db.execute(select(Child))
    children = child_result.scalars().all()
    
    # Получаем количество учителей
    teacher_result = await db.execute(select(Teacher))
    teachers = teacher_result.scalars().all()
    
    # Получаем количество достижений
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
    """
    Получить рейтинг муниципалитетов с детализацией по школам
    """
    try:
        # Сначала получаем все муниципалитеты
        municipalities = list(UserCity) if not city else [city]
        
        # Создаем алиасы для связанных таблиц
        child_alias = aliased(Child)
        achievement_alias = aliased(Achievement)
        
        # Вычисляем коэффициент непосредственно в SQL
        ratio_expr = (
            # Тип достижения
            case(
                (achievement_alias.type == AchieveType.SCIENCE, 1.4),
                (achievement_alias.type == AchieveType.ART, 1.4),
                (achievement_alias.type == AchieveType.SPORT, 1.4),
                else_=1.4
            ) *
            # Уровень достижения
            case(
                (achievement_alias.level == AchieveLevel.MUN, 1.25),
                (achievement_alias.level == AchieveLevel.INTER_MUN, 1.5),
                (achievement_alias.level == AchieveLevel.REGION, 2.25),
                (achievement_alias.level == AchieveLevel.INTER_REG, 3.75),
                (achievement_alias.level == AchieveLevel.ALL_RUS, 4.5),
                else_=1.25
            ) *
            # Формат достижения
            case(
                (achievement_alias.format == AchieveFormat.REMOTE, 0.5),
                (achievement_alias.format == AchieveFormat.OWN, 1.5),
                else_=0.5
            ) *
            # Команда
            case(
                (achievement_alias.team == AchieveTeam.SOLO, 1.75),
                (achievement_alias.team == AchieveTeam.TEAM, 1.25),
                else_=1.25
            ) *
            # Место
            case(
                (achievement_alias.place == AchievePlace.GRAN, 1.3),
                (achievement_alias.place == AchievePlace.FIRST, 1.25),
                (achievement_alias.place == AchievePlace.SECOND, 0.75),
                (achievement_alias.place == AchievePlace.THIRD, 0.5),
                (achievement_alias.place == AchievePlace.PARTICLANT, 0.25),
                else_=0.25
            )
        )
        
        # ВАЖНОЕ ИСПРАВЛЕНИЕ: Используем правильное имя алиаса в текстовом выражении
        # Заменяем "achievement.date" на "achievement_1.date"
        date_ratio_expr = case(
            # Более 3 лет - 0.0
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 1095"), 0.0),
            # От 2 до 3 лет - 0.25
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 730"), 0.25),
            # От 1 до 2 лет - 0.75
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 365"), 0.75),
            # От 30 дней до 1 года - 1.25
            (text("EXTRACT(DAY FROM CURRENT_DATE - achievement_1.date) > 30"), 1.25),
            # Менее 30 дней - 1.5
            else_=1.5
        )
        
        # Полный коэффициент
        total_ratio_expr = ratio_expr * date_ratio_expr
        
        # Собираем данные для всех муниципалитетов
        municipalities_data = []
        
        for city in municipalities:
            # Получаем школы в этом муниципалитете
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
            
            # Формируем список школ
            schools = []
            for index, (school_id, name, city, total_ratio) in enumerate(school_ratings, 1):
                schools.append({
                    "school_id": school_id,
                    "name": name,
                    "city": city,
                    "total_ratio": float(total_ratio) if total_ratio else 0.0,
                    "place": index
                })
            
            # Добавляем школы без достижений в этом городе
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
            
            # Сортируем школы по total_ratio
            schools.sort(key=lambda x: x["total_ratio"], reverse=True)
            
            # Обновляем места
            for index, school in enumerate(schools, 1):
                school["place"] = index
            
            # Вычисляем общий рейтинг муниципалитета
            total_municipality_ratio = sum(school["total_ratio"] for school in schools)
            
            municipalities_data.append({
                "city": city,
                "total_ratio": total_municipality_ratio,
                "schools": schools
            })
        
        # Сортируем муниципалитеты по total_ratio
        municipalities_data.sort(key=lambda x: x["total_ratio"], reverse=True)
        
        # Обновляем места для муниципалитетов
        for index, municipality in enumerate(municipalities_data, 1):
            municipality["place"] = index
            
        # Формируем окончательный ответ
        response = {
            "municipalities": municipalities_data
        }
        
        return response
    
    except Exception as e:
        print(f"Error in municipalities rating: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при получении рейтинга муниципалитетов")