from pydantic import BaseModel, EmailStr, Field


class CheckSubscription(BaseModel):
    chat_id: int
