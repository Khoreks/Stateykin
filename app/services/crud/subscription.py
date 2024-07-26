import datetime

from sqlalchemy.exc import IntegrityError

from models.subscription import UserSubscription, SubscriptionPlan
from database.session import get_database
from services.crud.user import get_user_by_chat_id


def get_all_subscriptions(db):
    subscriptions = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.is_active
    ).all()
    return subscriptions


def check_user_subscription(user, db) -> dict:
    subscription = user.subscribe
    if subscription.is_active and subscription.end_date < datetime.datetime.now():
        subscription.is_active = False
        db.commit()
        subscription = None

    return subscription


def check_chat_subscription(chat_id, db) -> dict:
    user = get_user_by_chat_id(chat_id=chat_id, db=db)
    subscription = check_user_subscription(user=user, db=db)

    return subscription


def init_subscriptions_plan() -> None:
    trial_subscription = SubscriptionPlan(
        name="Пробная",
        description="План предоставляет доступ к пробной версии сервиса генерации с лимитом 1 пост в сутки и сроком на 1 месяц",
        price=0.0,
        duration_month=1,
        day_limit=1
    )
    base_subscription = SubscriptionPlan(
        name="Базовая",
        description="План предоставляет доступ к генерации 4х постов в сутки сроком на 1 месяц",
        price=250.0,
        duration_month=1,
        is_free=False,
        day_limit=4
    )
    premium_subscription = SubscriptionPlan(
        name="Продвинутая",
        description="План предоставляет доступ к генерации 10 постов в сутки",
        price=500.0,
        duration_month=1,
        is_free=False,
        day_limit=10
    )

    db_generator = get_database()
    db_session = db_generator.__next__()

    for subscription in [trial_subscription, base_subscription, premium_subscription]:
        try:
            db_session.add(subscription)
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
