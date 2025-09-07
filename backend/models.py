from datetime import datetime, timezone
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(gt=4)
    hashed_password: int = Field(ge=8)

    messages: List['Message'] = Relationship(back_populates='user')


class Message(SQLModel, table=True):
    __tablename__ = 'messages'

    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    user_id: int = Field(foreign_key='users.id')
    user: User | None = Relationship(back_populates='messages')
