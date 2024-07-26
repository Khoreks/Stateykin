from pydantic import BaseModel
from typing import Any


class BaseResponse(BaseModel):
    success: bool = False  # Наличие ошибок при выполнении
    value: Any = None  # Результат успешного выполнения
    message: str = None  # Описание ошибки или доп информация
