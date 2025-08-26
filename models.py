from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str
    age: Optional[int] = None

class UserCreate(SQLModel):
    name: str
    username: str
    age: Optional[int] = None

class UserPatch(SQLModel):
    name: Optional[str] = None
    username: Optional[str] = None
    age: Optional[int] = None