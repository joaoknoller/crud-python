from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from db_config import get_session
from models import User, UserCreate, UserPatch

router = APIRouter(tags=["Users"])

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def index():
    return Path("index.html").read_text(encoding="utf-8")


@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    db_user = User.model_validate(user_create)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/", response_model=dict[str, List])
def read_users(session: Session = Depends(get_session)):
    db_users = session.exec(select(User)).all()
    return {"data": db_users}

@router.get("/users/{id}", response_model=User)
def read_user_by_id(id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, id)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    return db_user

@router.patch("/users/{id}", response_model=User)
def update_user(id: int, user_patch: UserPatch, session: Session = Depends(get_session)):
    db_user = session.get(User, id)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    patch_dict = user_patch.model_dump(exclude_unset=True)
    for key, value in patch_dict.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user 

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, id)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    session.delete(db_user)
    session.commit()

    return

