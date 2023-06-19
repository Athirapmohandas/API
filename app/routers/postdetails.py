from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List,Optional


router = APIRouter(
    # prefix="/post",
    tags=['Post']
)

# length
@router.get('/count',status_code=200,)
def get_count(db: Session = Depends(get_db),current_user: str = Depends(oauth2.get_current_user)):
    count=db.query(models.PostDetails).count()
    return {"total_records":count}

# length
@router.get('/countComments',status_code=200)
def get_count(db: Session = Depends(get_db)):
    result=(db.query(models.PostDetails.id,func.count(models.Comments.id)).outerjoin(models.PostDetails.comments).group_by(models.PostDetails.id).all())
    comments_count=[{
        'postdetails_id':models.PostDetails.id,'comments_count':count
    }
    for models.PostDetails.id, count in result]
    return comments_count


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.PostDetails, db: Session = Depends(get_db)):
    new_post = models.PostDetails( **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/post',status_code=200)
def get_data(limit:int=10,pageNumber:int=0,db: Session = Depends(get_db)):
    count=db.query(models.PostDetails).count()
    # posts_with_comment_details = db.query(models.PostDetails, func.count(models.Comments.id).label('comment_count')).outerjoin(models.Comments, models.PostDetails.id == models.Comments.postdetails_id).options(joinedload(models.PostDetails.comments)).group_by(models.PostDetails).order_by(models.PostDetails.id).limit(limit).offset(pageNumber*limit).all()
    posts_with_comment_details = db.query(models.PostDetails,func.count(models.Comments.id).label('comment_count'),models.PostLike.user_email).outerjoin(models.Comments, models.PostDetails.id == models.Comments.postdetails_id).outerjoin(
    models.PostLike, models.PostDetails.id == models.PostLike.post_id).options(joinedload(models.PostDetails.comments)).group_by(models.PostDetails,models.PostLike.user_email).order_by(models.PostDetails.id).limit(limit).offset(pageNumber*limit).all()
#     posts_with_comment_details = db.query(
#     models.PostDetails,
#     func.count(models.Comments.id).label('comment_count'),
#     models.PostLike.user_email
# ).outerjoin(models.Comments, models.PostDetails.id == models.Comments.postdetails_id).\
#     outerjoin(models.PostLike, models.PostDetails.id == models.PostLike.post_id).\
#     options(joinedload(models.PostDetails.comments)).\
#     group_by(models.PostDetails, models.PostLike.user_email).\
#     order_by(models.PostDetails.id).\
#     limit(limit).\
#     offset(pageNumber * limit).\
#     all()
    response = []
    post_dict = {}
    for post, comment_count,user_email in posts_with_comment_details:
      post_id=post.id
      liked_users = user_email.split(',') if user_email is not None else []
      if post_id in post_dict:
        post_dict[post_id]['liked_users'].extend(liked_users) 
      else:
        post_dict[post_id] = {
            'liked_users': liked_users,
            'comment_count': comment_count
        }

    for post_id, liked_users in post_dict.items():
        post = db.query(models.PostDetails).filter(models.PostDetails.id == post_id).first()
        count = db.query(models.PostDetails).count()
    
        liked_users_list = [str(user_email) for user_email in liked_users['liked_users']]  # Convert liked users to strings    
        post_details_out = schemas.PostDetailsOut3(
        postdetails=post,
        total_comments=liked_users['comment_count'],
        comments=post.comments[:2],
        total_posts=count,
        liked_users=liked_users_list
        )
    
        response.append(post_details_out)
    return response
        #   response.append(schemas.PostDetailsOut3(postdetails=post, total_comments=comment_count,comments=post.comments,total_posts=count))


# @router.get('/post',response_model=List[schemas.PostDetailsOut],status_code=200)
# def get_data(limit:int=10,pageNumber:int=0,tags:Optional[str]="",db: Session = Depends(get_db)):
#     items=db.query(models.PostDetails).filter(models.PostDetails.tags.contains([tags])).order_by(models.PostDetails.id).limit(limit).offset(pageNumber*limit).all()
#     return items

@router.get('/posts/{post_id}',response_model=schemas.PostDetailsOut2,status_code=200)
def get_data(post_id:int,db: Session = Depends(get_db)):
    items=db.query(models.PostDetails).filter(models.PostDetails.id==post_id).first()
    result=db.query(func.count(models.Comments.id)).outerjoin(models.PostDetails.comments).filter(models.Comments.postdetails_id==post_id).scalar()
    response=schemas.PostDetailsOut2(postdetails=items,total_posts=result)
    # raise exception
    if not items:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return response

@router.post("/comment", status_code=status.HTTP_201_CREATED)
def create_comments(post_id:int,comment: schemas.CommentsIn, db: Session = Depends(get_db)):
    new_comment = models.Comments(postdetails_id=post_id,**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# replies

@router.post("/replies", status_code=status.HTTP_201_CREATED)
def create_replies(replies: schemas.Replies, db: Session = Depends(get_db)):
    new_comment = models.Replies(**replies.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"success"}

# First 2 replies when limit <2
@router.get('/comments/{post_id}',status_code=200)
def get_data(post_id:int,limit:int=10,pageNumber:int=0,db: Session = Depends(get_db)):
    comments = db.query(models.Comments).filter(models.Comments.postdetails_id == post_id).limit(limit).offset(pageNumber*limit).all()
    comments_with_replies = []
    for comment in comments:
        replies = db.query(models.Replies).filter(models.Replies.comments_id == comment.id).all()
        reply_list = [schemas.Replies(comments_id=reply.comments_id,likes=reply.likes,replyname=reply.replyname, reply=reply.reply, user_email=reply.user_email) for reply in replies]
        comment_with_replies = schemas.CommentsOut1( comments=comment.comments,likes=comment.likes, user_email=comment.user_email, replies=reply_list[:2])
        comments_with_replies.append(comment_with_replies)

    return comments_with_replies

@router.get('/replies/{comment_id}',response_model=List[schemas.Replies],status_code=200)
def get_data(comment_id:int,limit:int=10,pageNumber:int=0,db: Session = Depends(get_db)):
    items=db.query(models.Replies).filter(models.Replies.comments_id==comment_id).limit(limit).offset(pageNumber*limit).all()
    return items

# @router.patch('/posts/{post_id}/{signal}',response_model=schemas.PostDetailsOut,status_code=200)
# def update_data(post_id:int,signal:str,db: Session = Depends(get_db)):
#     result=db.query(models.PostDetails).filter(models.PostDetails.id==post_id).first()
#     if(signal=='add'):
#         result.likes+=1
#     else:
#         result.likes-=1
#     db.commit()
#     db.refresh(result)
#     return result


# post like
@router.post('/postlike',status_code=status.HTTP_201_CREATED)
def postLike(vote:schemas.PostLike,db:Session= Depends (get_db)):
    post=db.query(models.PostDetails).filter(models.PostDetails.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")
    vote_query=db.query(models.PostLike).filter(models.PostLike.post_id==vote.post_id,models.PostLike.user_email==vote.user_email)
    found_vote = vote_query.first()
    if (vote.postliked == True):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {vote.user_email} has alredy liked on post {vote.post_id}")
        new_vote = models.PostLike(post_id=vote.post_id, user_email=vote.user_email)
        post.likes+=1
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist")
        post.likes-=1
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted like"}
    

# commentLike
@router.post('/commentlike',status_code=status.HTTP_201_CREATED)
def CommentLike(vote:schemas.CommentLike,db:Session= Depends (get_db)):
    comment=db.query(models.Comments).filter(models.Comments.id==vote.comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.comment_id} does not exist")
    vote_query=db.query(models.CommentLike).filter(models.CommentLike.comment_id==vote.comment_id,models.CommentLike.user_email==vote.user_email)
    found_vote = vote_query.first()
    if (vote.commentliked == True):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {vote.user_email} has alredy liked on comment {vote.comment_id}")
        new_vote = models.CommentLike(comment_id=vote.comment_id, user_email=vote.user_email)
        comment.likes+=1
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist")
        comment.likes-=1
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted like"}  



# ReplyLike
@router.post('/Replylike',status_code=status.HTTP_201_CREATED)
def ReplyLike(vote:schemas.ReplyLike,db:Session= Depends (get_db)):
    reply=db.query(models.Replies).filter(models.Replies.id==vote.reply_id).first()
    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.reply_id} does not exist")
    vote_query=db.query(models.ReplyLike).filter(models.ReplyLike.reply_id==vote.reply_id,models.ReplyLike.user_email==vote.user_email)
    found_vote = vote_query.first()
    if (vote.replyliked == True):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {vote.user_email} has alredy liked on reply {vote.reply_id}")
        new_vote = models.ReplyLike(reply_id=vote.reply_id, user_email=vote.user_email)
        reply.likes+=1
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist")
        reply.likes-=1
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted like"}  