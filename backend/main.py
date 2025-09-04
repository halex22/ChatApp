from contextlib import asynccontextmanager
from typing import Dict, Type

from auth import create_token, hash_password, verify_password
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from models import Message, User
from schemas import Credentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


@asynccontextmanager
async def create_tables(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=create_tables)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.post('/register')
async def sing_up(
    credentials: Credentials,
    db: AsyncSession = Depends(get_db)
) -> HTTPException | Dict[str, str]:
    result = await db.execute(select(User).where(User.username == credentials.user_name))
    if result.scalar():
        return HTTPException(status_code=400, detail='Username already taken')
    user = User(username=credentials.user_name,
                hashed_password=hash_password(credentials.password))
    db.add(user)
    await db.commit()
    return {'message': 'user created'}


@app.post('/login')
async def sing_in(
    credentials: Credentials,
    db: AsyncSession = Depends(get_db)
) -> HTTPException | Dict[str, str]:
    result = await db.execute(select(User).where(User.username == credentials.user_name))
    if not (user := result.scalar()):
        return HTTPException(status_code=400, detail='User not found')
    if not verify_password(credentials.password, user.hashed_password):
        return HTTPException(status_code=403, detail='Invalid credentials')
    token = create_token({'sub': user.username})
    return {'token': token}
