from cmath import exp
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
import schemas
# SECRET_KEY
# Algorithm
# Expiration time
SECRET_KEY = "bc5b41991eef9e0fbf9a2123e3548d92a244561255dfe9c71fc79c4f79db781a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("users_id")

        if id is None:
            raise credentials_exception
            
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

# def get_current_user(token: str = Depends())