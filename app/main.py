from fastapi import FastAPI

from tools.config import settings
from database.session import engine
from database import Base
from api import api_router
from services.crud.subscription import init_subscriptions_plan

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(api_router)


@app.on_event("startup")
def init_tables():
    Base.metadata.create_all(bind=engine)
    init_subscriptions_plan()


@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("\nApplication shutdown")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
