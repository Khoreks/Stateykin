from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database import Base


class SubscriptionPlan(Base):
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    duration_month = Column(Integer)
    is_free = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    day_limit = Column(Integer, nullable=False)


class UserSubscription(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    subscribe = relationship(SubscriptionPlan, uselist=False)
    subscribe_id = Column(Integer, ForeignKey("subscription_plan.id"), primary_key=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
