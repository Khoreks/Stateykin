from pydantic import BaseModel


class PostCreate(BaseModel):
    chat_id: int
    user_request: str
    topic: str
    platform: str
    audience: str
    additional_information: str
    extraction_information: str
    generate_search_request: str
    summarization_web_page: str
    generate: str
    feedback: int


class PostFeedback(BaseModel):
    chat_id: int
    post: str
    feedback: int
