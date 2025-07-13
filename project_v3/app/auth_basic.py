from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from .db import get_db
from .models_orm import UserORM

security = HTTPBasic(realm="Please enter your current username and password")

def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user = db.query(UserORM).filter(UserORM.username == credentials.username).first()
    if user is None or str(user.password) != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user 