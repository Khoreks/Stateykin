from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean

from database import Base


class Post(Base):
    chat_id = Column(Integer, ForeignKey("user.chat_id"), nullable=False, primary_key=True)
    user_request = Column(String)
    topic = Column(String)
    platform = Column(String)
    audience = Column(String)
    additional_information = Column(String)
    generate_search_request = Column(String)
    summarization_web_page = Column(String)
    generate = Column(String)
    feedback = Column(Integer)
