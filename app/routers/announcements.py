from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func, asc
from .. import models, schemas, oauth2
from ..database import get_db
from datetime import datetime,date
from typing import List,Optional

router = APIRouter(
    tags=['Announcemnets']
)


@router.get('/CommunityPostcount',status_code=200)
def get_count(db: Session = Depends(get_db)):
    result= db.query(models.PostDetails.community,func.count(models.PostDetails.community)).group_by(models.PostDetails.community)
    announcement_count=[{
        'community':community,'post_count':count
    }
        for community,count in result]
    return announcement_count     

@router.post('/CreateAnnouncement',response_model=schemas.Announcements)
def create_announcement(item:schemas.Announcements,db:Session = Depends(get_db)):
    new_item=models.Announcements(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.post('/Createcommunity',)
def create_community(item:str,db:Session = Depends(get_db)):
    new_item=models.Community(community_name=item)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get('/upcoming', response_model=List[schemas.Announcements])
def upcomingEVents(db:Session = Depends(get_db)):
    result= db.query(models.Announcements).filter(models.Announcements.event_date >= date.today()).order_by(models.Announcements.event_date.asc()).limit(5).all()
    return result
