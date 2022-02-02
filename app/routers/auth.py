from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app.oauth import create_access_token
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth

router=APIRouter(tags=['Login'])  

@router.post("/login",response_model=schemas.Token)
def login_user(user_credentials:dict,db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
   if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Invalid credentials")
   if not utils.verify(user_credentials.password,user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Invalid credentials")
   otp_verify=utils.verify(user_credentials.otp)
   if otp_verify is False:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Invalid credentials")
   access_token = oauth.create_access_token(data = {"user_id": user.id})
   return access_token
 
 




