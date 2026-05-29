from fastapi import APIRouter
from app.auth.schemas import UserCreate, UserResponse, UserInDB
from app.auth.hashing import hash_passwords
from app.database import cur,conn

router = APIRouter()

@router.post("/register")
def register(user_details:UserCreate):
    hashed_pass = hash_passwords(user_details.password)
    user_in_db = UserInDB(name=user_details.name,
                           email=user_details.email, hashed_password=hashed_pass)

    cur.execute("INSERT INTO users(name,email,hashed_password) " \
    "VALUES(%s,%s,%s)",(user_in_db.name,user_in_db.email,user_in_db.hashed_password))
    conn.commit()

    cur.execute("SELECT id from users WHERE email=%s",(user_in_db.email,))
    id = cur.fetchone()
    user_response = UserResponse(name=user_details.name,
                           email=user_details.email,id=id[0])

    return user_response