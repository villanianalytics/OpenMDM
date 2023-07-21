from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from security import authenticate

router = APIRouter()

# add your user-related endpoints here. For example:

@router.get("/user/me")
def read_me(user=Depends(authenticate)):
    return user
