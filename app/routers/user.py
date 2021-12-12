from os import error
from .. import models,schemas,utils,mail
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import  engine,get_db
from typing import Optional



router= APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def  create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
  hashed_password=utils.hash(user.password)
  user.password=hashed_password
  new_user=models.User(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  try:
    confirmation_mail=await mail.send_confirmation_email(user.email)
  except error:
     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Email couldn't be send.Please try again.")

  return confirmation_mail

@router.get("/{id}",response_model=schemas.UserOut)
def getuser(id:int,db: Session = Depends(get_db)):
  user=db.query(models.User).filter(models.User.id == id).first()
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with id: {id} was not found")

  return user  

