from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlmodel import Session, select

from db_config import create_db_and_tables, get_session
from models import User, UserRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📦 Creating tables...")
    create_db_and_tables()
    yield
    print("🧹 Shutdown application...")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return {"message": "Hello, FastAPI + SQLModel + SQLite!"}


@app.post("/users/", response_model=User)
def create_user(user: UserRequest, session: Session = Depends(get_session)):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.delete("/db/")
def delete_db(session: Session = Depends(get_session)):
    session.exec(text("DELETE FROM user"))
    session.commit()

    return {"message": "Success"}
