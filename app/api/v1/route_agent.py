import json

from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from schemas.response import BaseResponse
from schemas.agent import AgentInput
from schemas.post import PostFeedback
from database.session import get_database
from services.crud.subscription import check_chat_subscription
from services.crud.post import insert_post, insert_feedback
from services.crud.agent import worker_generation

router = APIRouter()


@router.post("/post/create", response_model=BaseResponse, status_code=200)
async def create_post(user_message: AgentInput, db: Session = Depends(get_database)):
    subscription = check_chat_subscription(chat_id=user_message.chat_id, db=db)

    if not subscription.is_active:
        return {
            "success": False,
            "message": "Отсутствует подписка",
            "value": None
        }

    # Проверка лимита
    # n = get_number_posts_per_day(chat_id=chat_id, db=db)
    # if n == subscription.limit:
    #     pass
    message_json = json.dumps({"user_message": user_message.message})

    generated_post = worker_generation(message_json)

    tg_post = generated_post["generation"]
    tg_post = tg_post.replace("**", "").replace("*", "•").replace("#", "")
    for i in ["!.?-"]:
        tg_post = tg_post.replace(i, "")
    post = {
        "chat_id": user_message.chat_id,
        "user_request": user_message.message,
        "topic": generated_post["topic"],
        "platform": generated_post["platform"],
        "audience": generated_post["audience"],
        "additional_information": generated_post["additional_information"],
        "generate_search_request": generated_post["web_search_queries"],
        "summarization_web_page": generated_post["context"],
        "generate": tg_post,
        "feedback": None
    }
    insert_post(post=post, db=db)

    return {
        "success": True,
        "message": "",
        "value": tg_post
    }


@router.post("/post/feedback", response_model=BaseResponse, status_code=200)
async def set_post_feedback(post_feedback: PostFeedback, db: Session = Depends(get_database)):
    try:
        insert_feedback(post_feedback=post_feedback, db=db)
        return {
            "success": True,
            "message": "",
            "value": None
        }
    except Exception as error:
        return {
            "success": False,
            "message": f"error: {error}",
            "value": None
        }
