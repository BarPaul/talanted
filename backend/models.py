from sqlalchemy import String, Boolean, Enum, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

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
        }[self]

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

    # TODO: паралелль из 2-х букв
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

    def __repr__(self):
        return f"Child(id={self.id}, name={self.name}, grade_id={self.grade_id})"

class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    school_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    school: Mapped["User"] = relationship(back_populates="teachers")

    def __repr__(self):
        return f"Teacher(id={self.id}, name={self.name}, school_id={self.school_id})"
