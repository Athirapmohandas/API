from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName= Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    # class Config:
    #        orm_mode=True
    

# class ChartData(Base):
#     __tablename__ = "chartdata"
#     id = Column(Integer, primary_key=True, nullable=False)
#     value= Column(Integer, nullable=False)
#     labels= Column(String,nullable=False)


# class ChartData1(Base):
#     __tablename__ = "chartdata1"
#     id = Column(Integer, primary_key=True, nullable=False)
#     value= Column(Integer, nullable=False)
    # labels= Column(String,nullable=False)

    # class Config:
    #        orm_mode=True

# class Post(Base):
#     __tablename__ = "post"
#     id = Column(Integer, primary_key=True, nullable=False)
#     content= Column(String(255), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text('now()'))
#     topic=Column(String, nullable=False)
#     # owner_id= Column(String, nullable=False)

#     owner_id = Column(Integer, ForeignKey(
#         "users.id", ondelete="CASCADE"), nullable=False)
#     owner = relationship("User")

class Comments(Base):
     __tablename__="comments"
     id=Column(Integer, primary_key=True, nullable=False)
     comments=Column(String(255), nullable=False)
     likes=Column(Integer,nullable=False)
     user_email = Column(String, ForeignKey("azureusers.email", ondelete="CASCADE"))
     postdetails_id=Column(Integer, ForeignKey(
        "postdetails.id", ondelete="CASCADE"), nullable=False)
     postdetails= relationship("PostDetails",back_populates="comments")
     replies=relationship("Replies",back_populates="comments")
     commentlikes = relationship("CommentLike", backref="Comments")



class Replies(Base):
     __tablename__="reply"
     id=Column(Integer, primary_key=True, nullable=False)
     reply=Column(String(255), nullable=False)
     likes=Column(Integer, nullable=False)
     replyTo=Column(String,nullable=True)
     comments_id=Column(Integer, ForeignKey(
        "comments.id", ondelete="CASCADE"), nullable=False)    
     comments= relationship("Comments",back_populates="replies")
     user_email = Column(String, ForeignKey("azureusers.email", ondelete="CASCADE"))
    #  owner=relationship("AzureUser",back_populates="reply")

 




class PostDetails(Base):
        __tablename__ = "postdetails"
        id=Column(Integer, primary_key=True, nullable=False)
        created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
        question=Column(String(255), nullable=False)
        title=Column(String(255), nullable=False)
        tags=Column(ARRAY(String), nullable=False)
        likes=Column(Integer, nullable=False)
        comments= relationship("Comments",back_populates="postdetails")
        community= Column(String(255), nullable=False)
        owner_email=Column(String, ForeignKey("azureusers.email", ondelete="CASCADE"),nullable=False)
        owner=relationship("AzureUser",back_populates="postdetails")
        postlikes = relationship("PostLike", backref="postdetails")

class AzureUser(Base):
      __tablename__="azureusers"
    #   id = Column(Integer, primary_key=True, nullable=False)
      firstName = Column(String, nullable=False)
      lastName= Column(String,nullable=False)
      email = Column(String, nullable=False,primary_key=True, unique=True)
      postdetails= relationship("PostDetails",back_populates="owner")

class PostLike(Base):
        __tablename__ = "postlike"
        user_email = Column(String, ForeignKey("azureusers.email", ondelete="CASCADE"), primary_key=True)
        post_id = Column(Integer, ForeignKey("postdetails.id", ondelete="CASCADE"), primary_key=True)
        
class CommentLike(Base):
        __tablename__ = "commentlike"
        user_email = Column(String, ForeignKey("azureusers.email", ondelete="CASCADE"), primary_key=True)
        comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True)

       
class ReplyLike(Base):
        __tablename__ = "Replylike"
        user_email = Column(String, ForeignKey("azureusers.email", ondelete="CASCADE"), primary_key=True)
        reply_id = Column(Integer, ForeignKey("reply.id", ondelete="CASCADE"), primary_key=True)
    
    







