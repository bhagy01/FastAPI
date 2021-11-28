from sqlalchemy.sql.expression import label
from sqlalchemy.sql.functions import func
from .. import models,schemas,utils,oauth
from typing import List, Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import  engine,get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)
# ,response_model=List[schemas.Post]
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user),limit:int = 10,skip:int =0,search:Optional[str] = ""):
  #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  results = db.query(models.Post,func.count(models.Vote.post_id).label("Votes") ).join(models.Vote,models.Post.id== models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  #cursor.execute(""" select * from users""")
  #posts=cursor.fetchall()
  return  results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostBase,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute(""" Insert into users (title,content,published) values(%s,%s,%s)  returning * """ , (post.title,post.content,post.published))
    # new_posts=cursor.fetchone()
    # conn.commit()
    new_posts=models.Post(user_id=current_user.id,**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return  new_posts  
 
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
  #  cursor.execute("""select * from users where id = %s """ , (str(id)))
  #  post=cursor.fetchone()
 post= db.query(models.Post,func.count(models.Vote.post_id).label("Votes") ).join(models.Vote,models.Post.id== models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

 if not post:
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail= f"Post with id: {id} was not found")
 return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
  # cursor.execute("""delete from users where id = %s returning * """ , (str(id)))
  # post=cursor.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id: {id} was not found") 
  if post.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to delete")
  post_query.delete(synchronize_session=False)
  db.commit()
  return  Response (status_code=status.HTTP_204_NO_CONTENT)
 
 

@router.put("/{id}",response_model=schemas.Post)
def update_post(updated_post:schemas.PostCreate,id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
  # cursor.execute("""update users set title = %s,content = %s where id = %s returning * """ , (post.title,post.content,str(id)))
  # updated_post=cursor.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id: {id} was not found")
  if post.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to update others post")
  post_query.update(updated_post.dict(),synchronize_session=False)
  db.commit()
  return post