from pydantic import BaseModel, EmailStr, Field


class AgentInput(BaseModel):
    chat_id: int
    message: str
