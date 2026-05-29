from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_passwords(password):
    return pwd_context.hash(password)

def check_password(user_entered_password,actual_password):
    return pwd_context.verify(user_entered_password,actual_password)
