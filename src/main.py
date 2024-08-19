"""
Точка входа.
"""

from fastapi import FastAPI

from src.car.router import router as router_chat

from starlette.middleware.cors import CORSMiddleware
from src.config import ALLOWED_ORIGINS

from contextlib import asynccontextmanager

from src.database import create_tables

# ДОПИСАТ�� БЛ��Т�� УЕБОК НА��У��
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('Таблица создана или уже была создана ранее')
    yield
    print('Выключение')

app = FastAPI(lifespan=lifespan)

origins = ALLOWED_ORIGINS.split(';')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'],
                   allow_headers=['*'], allow_credentials=True)


app.include_router(router_chat)



@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.get("/ping", include_in_schema=False)
async def health():
    return {"msg": "mxnzEgBjbUQSNE9i8dfk"}
