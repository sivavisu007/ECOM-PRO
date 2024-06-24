from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import crud
import models
from database import sessionlocal
from passlib.context import CryptContext
import os
from datetime import timezone, datetime, timedelta
from typing import Annotated 
secret_key = str(os.getenv('SECRET_KEY'))
algorithm = str(os.getenv('ALGORITHM'))
access_token_expire = int(400)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return bcrypt_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def get_user(db: Session, username: str):
    return crud.get_user_by_username(db, username)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    user = get_user(db, username)
    if user is None:
        raise exception
    return user