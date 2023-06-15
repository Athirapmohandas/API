from fastapi import APIRouter, Depends, status, HTTPException, Response,Header
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

security = HTTPBearer()
# @router.post('/login', response_model=schemas.Token)
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

#     user = db.query(models.User).filter(
#         models.User.email == user_credentials.username).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

#     # create a token
#     # return token

#     access_token = oauth2.create_access_token(data={"user_id": user.id})

#     return {"access_token": access_token, "token_type": "bearer"}


@router.post('/getToken',response_model=schemas.Token)
def getToken(username:schemas.AzureUser,db:Session=Depends(database.get_db)):
    user = db.query(models.AzureUser).filter(models.AzureUser.email==username.user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid username")
    access_token = oauth2.create_access_token(data={"user_id": username.user_email})
    return {"access_token": access_token, "token_type": "bearer"}

