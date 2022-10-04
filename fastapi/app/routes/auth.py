
from msilib import schema
from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
import utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def user_login(user_credentials: schemas.UserLogin, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
        
    return {"token":"example token"}