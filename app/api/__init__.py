from fastapi import APIRouter

from api.v1 import route_user, route_subscription, route_agent

api_router = APIRouter()
api_router.include_router(route_user.router, prefix="", tags=["Users"])
api_router.include_router(route_subscription.router, prefix="", tags=["Subscribe"])
api_router.include_router(route_agent.router, prefix="", tags=["Agent"])
