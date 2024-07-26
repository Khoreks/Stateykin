from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from database.session import get_database
from schemas.response import BaseResponse
from services.crud.subscription import check_user_subscription, get_all_subscriptions, check_chat_subscription
from schemas.subscription import CheckSubscription

router = APIRouter()


@router.post("/subscription/check", response_model=BaseResponse)
async def check_subscription(user_subscription: CheckSubscription, db: Session = Depends(get_database)):
    subscription = check_chat_subscription(chat_id=user_subscription.chat_id, db=db)

    if subscription:
        msg = f"""Ваша подписка - «{subscription.subscribe.name}»
Срок действия до {subscription.end_date.strftime('%d.%m.%Y, %H:%M:%S')}
Лимит - {subscription.subscribe.day_limit} \
{'генерация' if subscription.subscribe.day_limit == 1 else 'генераций'} в день"""
        return {
            "success": True,
            "message": msg,
            "value": True
        }
    else:
        return {
            "success": True,
            "message": "У Вас нет активной подписки",
            "value": False
        }


@router.get("/subscription/list", response_model=BaseResponse)
async def subscription_list(db: Session = Depends(get_database)):
    subscriptions = get_all_subscriptions(db)
    return {
        "success": True,
        "value": subscriptions
    }
