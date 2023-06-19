from sqlalchemy import Column, Integer, String, ForeignKey, Date
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
     replyname=Column(String,nullable=True)
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
        team =Column(String(255), nullable=False)
        content=Column(String(255), nullable=False)
        name=Column(String(255), nullable=False)
        tags=Column(ARRAY(String), nullable=False)
        likes=Column(Integer, nullable=False)
        comments= relationship("Comments",back_populates="postdetails")
        community= Column(String, ForeignKey("community.community_name", ondelete="CASCADE"))
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


class Announcements(Base):
       __tablename__="announcements"
       id=Column(Integer, primary_key=True, nullable=False)
       community= Column(String, ForeignKey("community.community_name", ondelete="CASCADE"))
       event_date=Column(Date,nullable=False)
       content=Column(String(255),nullable=False)
       created_at = Column(TIMESTAMP(timezone=True),
                        nullable=True, server_default=text('now()'))

    
class Community(Base):
        __tablename__="community"
        community_name=Column(String(255),nullable=False,primary_key=True)






