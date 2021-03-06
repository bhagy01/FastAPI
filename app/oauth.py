from fastapi.exceptions import HTTPException
from jose import jwt,JWSError
from datetime import datetime,timedelta
from jose.constants import Algorithms
from jose.exceptions import JWTError
from fastapi import Depends,HTTPException,status
from app import models,schemas
from app.config import Settings
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" :expire})
    jwt_token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return { "access_token":jwt_token , "token_type": "bearer"}

def verify_access_token(token:str,credentials_exception):
    try:
     payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
     print(payload)
     id:str =payload.get("user_id")
     if id is None:
        raise credentials_exception
     token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    print(token)
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user


     


