from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base
from models.subscription import UserSubscription


class User(Base):
    login = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    subscribe = relationship(UserSubscription, uselist=False)
