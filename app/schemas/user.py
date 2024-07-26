from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    login: str
    chat_id: int
    first_name: str
    last_name: str


class ShowUser(BaseModel):
    id: int
    login: str
    is_active: bool

    class Config():
        orm_mode = True
