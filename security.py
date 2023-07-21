from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets
from database import SessionLocal
from models import User

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None or not secrets.compare_digest(user.password, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user
