from fastapi import FastAPI
from domain.manager import router

app = FastAPI()

app.include_router(router)
