from fastapi import HTTPException, Depends, status
from passlib.context import CryptContext 


SECRET_KEY = "7576a5fb4dec953d694206811b7ed1d87f16953a52f6093541e6d7a7bbbb1b7b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#this string is used to hash passwords and defines the scheme to be used
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")


#compares both passwords' hashes
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def  get_password_hash(password):
    return pwd_context.hash(password)

