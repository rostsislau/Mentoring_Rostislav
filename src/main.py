from fastapi import FastAPI
from db.__init__ import init_db
from web.api.v1.task import router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router, prefix="/api/v1", tags=["tasks"])
