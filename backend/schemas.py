from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class Credentials:
    user_name: str = Field(min_length=4)
    password: str = Field(min_length=8)


@dataclass
class PublicUser:
    user_name: str = Field(min_length=4)
    id: int
