from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password:str
class UserInDB(BaseModel):
    name:str
    email:str
    hashed_password: str

class UserResponse(BaseModel):
    name:str
    email:str
    id:int

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token : str
    token_type:str = "bearer"