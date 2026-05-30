from fastapi import APIRouter,HTTPException,status, Depends
from .schemas import UserCreate , UserInDB , UserResponse, LoginRequest, Token
from .hashing import hash_passwords , check_password
from app.database import cur,conn
from .token import create_access_token , verify_access_token, get_current_user

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


@router.post("/login")
def login(login_details:LoginRequest):
        cur.execute("SELECT hashed_password from users WHERE email=%s",(login_details.email,))
        hashed_pass = cur.fetchone()
        if(hashed_pass==None):
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User doesn't exist")
        else:
              if check_password(login_details.password,hashed_pass[0]):
                    access_token = create_access_token({"sub":login_details.email})
                    login_response = Token(access_token=access_token)
                    return login_response
              else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password entered")
              

@router.get("/me")
def me(current_user: str = Depends(get_current_user)):
      return {"email":current_user}
      