from fastapi import FastAPI

from .web.api.v1.task import router

app = FastAPI()


app.include_router(router, prefix="/api", tags=["tasks"])
