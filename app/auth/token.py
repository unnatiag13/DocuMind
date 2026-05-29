import jwt
from dotenv import load_dotenv
import os
from fastapi import HTTPException , status , Depends
from fastapi.security import OAuth2PasswordBearer
import datetime

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict,expires_delta:int=30):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expires_delta)
    data["exp"] = expire
    token = jwt.encode(data,os.getenv("SECRET_KEY"),os.getenv("ALGORITHM"))
    return token


def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,os.getenv("SECRET_KEY"),algorithms=[os.getenv("ALGORITHM")])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    return payload["sub"]

