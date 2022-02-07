from os import error
from .. import models,schemas,utils,mail,oauth
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import  engine,get_db
from typing import Optional
from jose import jwt
from ..config import settings



router= APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def  create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
  # CHECK IF USER ALREADY EXISTS
  user_present = db.query(models.User).filter(models.User.email == user.email).first()
  if user_present is not None:
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=" User already exists")
  hashed_password=utils.hash(user.password)
  user.password=hashed_password
  new_user=models.User(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  confirmation_token = oauth.create_access_token(data = {"user_id": new_user.id})
  token=confirmation_token.get("access_token")
  try:
    confirmation_mail=await mail.send_confirmation_email(token,new_user.email)
  except error:
     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Email couldn't be send.Please try again.")

  return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def getuser(id:int,db: Session = Depends(get_db)):
  user=db.query(models.User).filter(models.User.id == id).first()
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with id: {id} was not found")

  return user  

@router.get("/verify/{token}",response_model=schemas.UserOut)
def verify_user(token:str,db: Session = Depends(get_db)):
  try:
    payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
  except jwt.JWSError:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has Expired")
  id:str =payload.get("user_id")
  print(payload)
  user_query = db.query(models.User).filter(models.User.id == id)
  user = user_query.first()
  if user is None:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist")
  if user.is_active == True:
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already Activated")
  update_is_active=user_query.update({models.User.is_active: True},synchronize_session=False)
  db.commit()
  return user

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,current_user: int = Depends(oauth.get_current_user),db: Session = Depends(get_db)):
  user_find=db.query(models.User).filter(models.User.id == id)
  user = user_find.first()
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
  if user.id != current_user.id:
   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to delete")
  user_find.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
  
