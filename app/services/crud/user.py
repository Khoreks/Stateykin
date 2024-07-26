import datetime

from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from schemas.user import UserCreate
from models.user import User
from models.subscription import UserSubscription, SubscriptionPlan


def create_new_user(user: UserCreate, db):
    user = User(
        login=user.login,
        first_name=user.first_name,
        last_name=user.last_name,
        chat_id=user.chat_id,
        is_active=True
    )
    trial_subscribe = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.is_free & SubscriptionPlan.is_active
    ).first()
    subscribe = UserSubscription(
        user_id=user.id,
        subscribe=trial_subscribe,
        subscribe_id=trial_subscribe.id,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now() + datetime.timedelta(weeks=trial_subscribe.duration_month * 4)
    )
    user.subscribe = subscribe
    try:
        db.add(user)
        db.add(subscribe)
        db.commit()
        db.refresh(user)
        return user
    except UniqueViolation:
        return None
    except IntegrityError:
        return None


def get_user_by_chat_id(chat_id, db):
    user = db.query(User).filter(
        (User.chat_id == chat_id)
    ).first()
    return user
