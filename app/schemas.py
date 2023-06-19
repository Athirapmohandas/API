from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime,date
from typing import Optional, List
from pydantic.types import conint


class UserCreate(BaseModel):
    firstName:str
    lastName:str
    email: EmailStr
    password: str
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# class ChartData(BaseModel):
#     labels: str
#     value: int

#     class Config:
#         orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

# class Post(BaseModel):
#     content: str
#     created_at: datetime
#     topic:str
#     owner_id:str
#     owner:UserOut


#     class Config:
#         orm_mode = True

# class PostCreate(BaseModel):
#     content: str
#     topic:str
#     created_at: datetime


#     class Config:
#         orm_mode = True
class CommentsIn(BaseModel):
    comments:str
    likes:int
    user_email:EmailStr
    class Config:
        orm_mode = True

class Comments(BaseModel):
    id:Optional[int]
    comments:str
    likes:int
    user_email:EmailStr
    class Config:
        orm_mode = True



class Replies(BaseModel):
    comments_id:int
    reply:str
    likes:int
    user_email:EmailStr
    replyname: Optional[str]
    class Config:
        orm_mode = True

class PostDetails(BaseModel):
    created_at: datetime
    content:str
    team:str
    name:str
    tags:list[str]
    likes:int
    owner_email:EmailStr
    community:str
    class Config:
        orm_mode = True
  

class PostOut(PostDetails):
    id:int       
   


class CommentsOut(Comments):
     comments:str
     likes:int
    #  views:int
     replies:List[Replies]=[]
     @validator('replies')
     def validate_replies(cls, replies):
        if len(replies) > 2:
            return replies[:2]
        return replies
     class Config:
        orm_mode = True 

class CommentsOut1(BaseModel):
     comments:str
     likes:int
     user_email:EmailStr
     replies:List[Replies]=[]
     class Config:
        orm_mode = True 

class PostDetailsOut(PostDetails):
      id:int
      comment:List[Comments]=[]
    #   count:int
    #   answers:List[Answers]=[]
      
      class Config:
        orm_mode = True 


class PostDetailsOut1(BaseModel):
      total_posts:int
      postdetails:List[PostDetailsOut]
      total_comments:int
      
      class Config:
        orm_mode = True 

class PostDetailsOut2(BaseModel):
      total_posts:int= Field(default=0)
      postdetails:PostDetailsOut
      
      class Config:
        orm_mode = True 

class PostLike(BaseModel):
      user_email:EmailStr
      post_id:int
      postliked:bool
    #   dir:conint(le=1)
      class Config:
        orm_mode = True 

class PostLikeOut(BaseModel):
      dir:conint(le=1)
      class Config:
        orm_mode = True 
      
class PostDetailsOut3(BaseModel):
      total_posts:int
      postdetails:PostOut
      total_comments:int= Field(default=0)
      postlikes:List[PostLikeOut]=[]
      liked_users: Optional[List[str]]
      comments:List[CommentsOut]=[]
      
      class Config:
        orm_mode = True 



class AzureUser(BaseModel):
    firstName:str
    lastName:str
    email:EmailStr

    class Config:
        orm_mode = True 


class CommentLike(BaseModel):
    comment_id:int
    user_email:EmailStr
    commentliked:bool
    # dir:conint(le=1)

class ReplyLike(BaseModel):
    reply_id:int
    user_email:EmailStr
    # dir:conint(le=1)
    replyliked:bool

class PostDetails1(BaseModel):
      id:int
      name:str
      
class Comments1(BaseModel):
    id:int
    comments:str
    postdetails_id:int

class PostLike1(BaseModel):
    post_id:int
    user_email:EmailStr

class CommentLike1(BaseModel):
    comment_id:int
    user_email:EmailStr

class ReplyLike1(BaseModel):
    reply_id:int
    user_email:EmailStr

class UserHistory(BaseModel):
    user_email: str
    post_history: List[PostDetails1]
    comment_history: List[Comments1]
    post_like_history: List[PostLike1]
    comment_like_history: List[CommentLike1]
    reply_like_history: List[ReplyLike1]


    # like_history: List[Like]

class Announcements(BaseModel):
    community:str
    event_date:date
    content:str
    created_at: datetime
    class Config:
        orm_mode = True



