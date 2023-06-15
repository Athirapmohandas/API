# from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# from sqlalchemy.orm import Session
# from .. import models, schemas, utils
# from ..database import get_db
# from typing import List


# router = APIRouter(
#     # prefix="/data",
#     tags=['data']
# )
# @router.get('/data',response_model=List[schemas.ChartData],status_code=200)
# def get_vessel_details(db: Session = Depends(get_db)):
#     items=db.query(models.ChartData).all()
#     return items

# @router.post('/data',status_code=status.HTTP_201_CREATED)
# def add_vessel(data:schemas.ChartData, db:Session=Depends(get_db)):
#     data=models.ChartData(
#       **data.dict()
#         )
#     db.add(data)
#     db.commit()
#     return {"status":"success"}

# @router.get('/data1',response_model=List[schemas.ChartData],status_code=200)
# def get_vessel_details(db: Session = Depends(get_db)):
#     items=db.query(models.ChartData1).all()
#     return items

# @router.post('/data1',status_code=status.HTTP_201_CREATED)
# def add_vessel(data:schemas.ChartData, db:Session=Depends(get_db)):
#     data=models.ChartData1(
#       **data.dict()
#         )
#     db.add(data)
#     db.commit()
#     return {"status":"success"}