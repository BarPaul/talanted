from sqlalchemy import String, Boolean, Enum, Integer, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
import datetime

Base = declarative_base()

class UserRole(str, enum.Enum):
    OWNER = "owner"
    MUN = "mun"
    SCHOOL = "school"

    @property
    def level(self) -> int:
        return {
            UserRole.SCHOOL: 1,
            UserRole.MUN: 2,
            UserRole.OWNER: 3
        }.get(self, 0)

class UserCity(str, enum.Enum):
    ALEXANDROVSK = "Александровск"
    ALMAZNAYA = "Алмазная"
    ALCHEVSK = "Алчевск"
    ANTRATSIT = "Антрацит"
    ARTYOMOVSK = "Артёмовск"
    BRYANKA = "Брянка"
    VAKHRUSHEVO = "Вахрушево"
    GORSKOE = "Горское"
    ZIMOGORIE = "Зимогорье"
    ZOLOTOE = "Золотое"
    ZORINSK = "Зоринск"
    IRMINO = "Ирмино"
    KIROVSK = "Кировск"
    KRASNODON = "Краснодон"
    KRASNY_LUCH = "Красный Луч"
    KREMENNAYA = "Кременная"
    LISICHANSK = "Лисичанск"
    LUGANSK = "Луганск"
    LUTUGINO = "Лутугино"
    MIUSINSK = "Миусинск"
    MOLODOGVARDEYSK = "Молодогвардейск"
    NOVODRUZHESK = "Новодружеск"
    PERVOMAISK = "Первомайск"
    PEREVALSK = "Перевальск"
    PETROVSKOE = "Петровское"
    POPASNAYA = "Попасная"
    PRIVOLIE = "Приволье"
    ROVENKI = "Ровеньки"
    RUBEZHNOE = "Рубежное"
    SVATOVO = "Сватово"
    SVERDLOVSK = "Свердловск"
    SEVERODONETSK = "Северодонецк"
    STAROBELSK = "Старобельск"
    STAKHANOV = "Стаханов"
    SUKHODOLSK = "Суходольск"
    SCHASTIE = "Счастье"
    CHERVONOPARTIZANSK = "Червонопартизанск"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.SCHOOL)
    city: Mapped[UserCity] = mapped_column(Enum(UserCity), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    grades: Mapped[list["Grade"]] = relationship(back_populates="school")
    teachers: Mapped[list["Teacher"]] = relationship(back_populates="school")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, name={self.name}, city={self.city}, role={self.role}, is_active={self.is_active})"

class Grade(Base):
    __tablename__ = "grade"

    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    parallel: Mapped[str] = mapped_column(String(1), nullable=False)
    school_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    school: Mapped[User] = relationship(back_populates="grades")
    children: Mapped[list["Child"]] = relationship(back_populates="grade")

    __table_args__ = (
        CheckConstraint('grade >= 1 AND grade <= 11', name='check_grade_range'),
        CheckConstraint("parallel BETWEEN 'А' AND 'Я'", name='check_parallel_letter'),
    )

    def __repr__(self):
        return f"Grade(id={self.id}, grade={self.grade}, parralel={self.parallel}, school_id={self.school_id})"

class Child(Base):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    grade_id: Mapped[int] = mapped_column(ForeignKey("grade.id", ondelete="SET NULL"), nullable=False)
   
    grade: Mapped[Grade] = relationship(back_populates="children")
    achievements: Mapped[list["Achievement"]] = relationship(back_populates="child")

    def __repr__(self):
        return f"Child(id={self.id}, name={self.name}, grade_id={self.grade_id})"

class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    school_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    school: Mapped["User"] = relationship(back_populates="teachers")
    achievements: Mapped[list["Achievement"]] = relationship(back_populates="teacher")

    def __repr__(self):
        return f"Teacher(id={self.id}, name={self.name}, school_id={self.school_id})"

class AchieveRatio(str, enum.Enum):
    @property
    def ratio(self) -> float:
        pass

class AchieveType(AchieveRatio):
    SCIENCE = "Наука"
    ART = "Искусство"
    SPORT = "Спорт"

    @property
    def ratio(self) -> float:
        return {
            AchieveType.SCIENCE: 1.4,
            AchieveType.ART: 1.4,
            AchieveType.SPORT: 1.4
        }.get(self, 1.4)

class AchieveLevel(AchieveRatio):
    MUN = "Городской"
    INTER_MUN = "Межгородской"
    REGION = "Региональный"
    INTER_REG = "Межрегиональный"
    ALL_RUS = "Всероссийский"

    @property
    def ratio(self) -> float:
        return {
            AchieveLevel.MUN: 1.25,
            AchieveLevel.INTER_MUN: 1.5,
            AchieveLevel.REGION: 2.25,
            AchieveLevel.INTER_REG: 3.75,
            AchieveLevel.ALL_RUS: 4.5
        }.get(self, 1.25)

class AchieveFormat(AchieveRatio):
    REMOTE = "Дистанционное"
    OWN = "Очное"

    @property
    def ratio(self) -> float:
        return {
            AchieveFormat.REMOTE: 0.5,
            AchieveFormat.OWN: 1.5,
        }.get(self, 0.5)

class AchieveTeam(AchieveRatio):
    TEAM = "Комадное"
    SOLO = "Одиночное"

    @property
    def ratio(self) -> float:
        return {
            AchieveTeam.SOLO: 1.75,
            AchieveTeam.TEAM: 1.25
        }.get(self, 1.25)

class AchievePlace(AchieveRatio):
    GRAN = "Гран при"
    FIRST = "1-е место"
    SECOND = "2-е место"
    THIRD = "3-е место"
    PARTICLANT = "участник"

    @property
    def ratio(self) -> float:
        return {
            AchievePlace.GRAN: 1.3,
            AchievePlace.FIRST: 1.25,
            AchievePlace.SECOND: 0.75,
            AchievePlace.THIRD: 0.5,
            AchievePlace.PARTICLANT: 0.25,
        }.get(self, 0.25)


class Achievement(Base):
    __tablename__ = "achievement"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[AchieveType] = mapped_column(Enum(AchieveType), nullable=False)
    level: Mapped[AchieveLevel] = mapped_column(Enum(AchieveLevel), nullable=False)
    format: Mapped[AchieveFormat] = mapped_column(Enum(AchieveFormat), nullable=False)
    team: Mapped[AchieveTeam] = mapped_column(Enum(AchieveTeam), nullable=False)
    place: Mapped[int] = mapped_column(Enum(AchievePlace), nullable=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("child.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    # verified: Mapped[bool] = mapped_column(Boolean, default=False)

    child: Mapped["Child"] = relationship("Child", back_populates="achievements", foreign_keys=[child_id])
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="achievements", foreign_keys=[teacher_id])

    __table_args__ = (
        CheckConstraint('date <= CURRENT_DATE', name='check_date_future'),
    )

    @property
    def ratio(self) -> float:
        base_ratio = 1
        for factor in (self.type, self.level, self.format, self.team, self.place):
            base_ratio *= factor.ratio
        return base_ratio * self.__date_ratio

    @property
    def __date_ratio(self) -> float:
        current_date = datetime.datetime.today()
        days_passed = (current_date - self.date).days
        if days_passed > 3 * 365:
            return 0.0
        elif days_passed > 2 * 365:
            return 0.25
        elif days_passed > 1 * 365:
            return 0.75
        elif days_passed > 30:
            return 1.25
        return 1.5

    def __repr__(self):
        return f"Achievement(id={self.id}, name={self.name}, ratio={self.ratio})"
