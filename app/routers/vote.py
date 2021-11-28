from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import  session
from .. import schemas,models,oauth
from app import database

router=APIRouter(
    prefix= "/vote",
    tags=["vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(Vote:schemas.Vote,db:session=Depends(database.get_db),current_user:int=Depends(oauth.get_current_user)):
    post =db.query(models.Post).filter(models.Post.id == Vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{Vote.post_id} not found")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==Vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if (Vote.dir == 1):
     if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} already voted on the post")  
     new_vote=models.Vote(post_id=Vote.post_id,user_id=current_user.id)  
     db.add(new_vote) 
     db.commit()
     return {"message": "successfully added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
        
        