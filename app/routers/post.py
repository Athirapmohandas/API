# from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# from sqlalchemy.orm import Session
# from .. import models, schemas, oauth2
# from ..database import get_db
# from typing import List


# router = APIRouter(
#     prefix="/forum",
#     tags=['forum']
# )

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
#     new_post = models.Post(owner_id=current_user.id, **post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


# @router.get('/',response_model=List[schemas.Post],status_code=200)
# def get_data(topic:str,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
#     items=db.query(models.Post).filter(models.Post.topic==topic).all()
#     return items