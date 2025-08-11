from fastapi import HTTPException

CREDENTIALS = HTTPException(
    status_code=401,
    detail="Аккаунт не авторизован!",
)

EMAIL = HTTPException(
    status_code=400, 
    detail="Данная почта уже зарегистрирована!"
)

NOT_ALLOWED = HTTPException(
    status_code=403, 
    detail="У аккаунта нет прав!"
)

NOT_EXISTS = HTTPException(
    status_code=404, 
    detail="Аккаунт не найден!"
)

NOT_ACTIVE = HTTPException(
    status_code=400, 
    detail="Аккаунт не активирован!"
)

ALREADY_ACTIVATED = HTTPException(
    status_code=409, 
    detail="Аккаунт уже активирован!"
)

WRONG_PASSWORD = HTTPException(
    status_code=400, 
    detail="Неверный пароль!"
)

SELF_DELETING = HTTPException(
    status_code=403,
    detail="Невозможно удалить собственный аккаунт!"
)

GRADE_NOT_EXISTS = HTTPException(
    status_code=404,
    detail="Класс не найден!"
)

TEACHER_NOT_EXISTS = HTTPException(
    status_code=404,
    detail="Учитель не найден!"
)

CHILD_NOT_EXISTS = HTTPException(
    status_code=404,
    detail="Ученик не найден!"
)

ACHIEVEMENT_NOT_EXISTS = HTTPException(
    status_code=404,
    detail="Достижение не найдено!"
)

WRONG_EXTENSION =  HTTPException(
    status_code=400, 
    detail="Недопустимый формат файла! Разрешены: *.pdf, *.jpg, *.jpeg, *.png"
)

IN_FUTURE = HTTPException(
    status_code=400, 
    detail="Дата достижения не может быть в будущем!"
)

WRONG_DATEFORMAT = HTTPException(
    status_code=400,
    detail="Неверный формат даты! Используйте ДД.ММ.ГГГГ"
)

TOO_OLDDATE = HTTPException(
    status_code=400,
    detail="Достижение слишком старое! Не более 3-х лет с получения"
)