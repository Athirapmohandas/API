from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/signup",
    tags=['Signup']
)

# /users/
# /users


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     email=db.query(models.User).filter(models.User.email == user.email).first()
#     if email != None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already exists")

#     # hash the password - user.password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AzureUser)
def create_user(user: schemas.AzureUser, db: Session = Depends(get_db)):
    email=db.query(models.AzureUser).filter(models.AzureUser.email == user.email).first()
    if email != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already exists")

    # hash the password - user.password
    # hashed_password = utils.hash(user.password)
    # user.password = hashed_password

    new_user = models.AzureUser(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/viewHistory',status_code=200)
def get_data(email:str,db: Session = Depends(get_db)):
     # Retrieve the user's post, comment, and liked history from the database
    posts = db.query(models.PostDetails).filter(models.PostDetails.owner_email==email).all()
    comments = db.query(models.Comments).filter(models.Comments.user_email==email).all()
    postlikes = db.query(models.PostLike).filter(models.PostLike.user_email==email).all()
    commentlikes = db.query(models.CommentLike).filter(models.CommentLike.user_email==email).all()
    replylikes = db.query(models.ReplyLike).filter(models.ReplyLike.user_email==email).all()

    # Prepare the response data
    post_history = []
    for post in posts:
        post_data = schemas.PostDetails1(id=post.id,title=post.title)
        post_history.append(post_data)

    comment_history = []
    for comment in comments:
        comment_data = schemas.Comments1(id=comment.id,comments=comment.comments,postdetails_id=comment.postdetails_id)
        comment_history.append(comment_data)

    like_history = []
    for like in postlikes:
        like_data = schemas.PostLike1(post_id=like.post_id, user_email=like.user_email)
        like_history.append(like_data)

    comment_like_history = []
    for like in commentlikes:
        like_data = schemas.CommentLike1(comment_id=like.comment_id, user_email=like.user_email)
        comment_like_history.append(like_data)

    reply_like_history = []
    for like in replylikes:
        like_data = schemas.ReplyLike1(reply_id=like.reply_id, user_email=like.user_email)
        reply_like_history.append(like_data)

    user_history = schemas.UserHistory(user_email=email, post_history=post_history, comment_history=comment_history,post_like_history=like_history,comment_like_history=comment_like_history,reply_like_history=reply_like_history)
    return user_history

