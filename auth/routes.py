from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError 
from sqlalchemy.orm import Session

from auth.schemas import CreateUsers, Token, TokenData
from auth.utils import (
    verify_password,
    get_password_hash,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from auth.models import Users
from auth.service import UserService
from database.service import get_db

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


def authenticate_user(db: Session, username: str, password: str):
    user = UserService.get_user_by_username(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Expire time is calculated and added to the payload
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    access_token = jwt.encode(
        {"sub": user.username, "exp": expire.timestamp()},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users")
def register_user(user: CreateUsers, db: Session = Depends(get_db)):
    existing_user = UserService.user_exists(db, user.username, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    new_user = UserService.create_user(db, user)
    return {"username": new_user.username, "email": new_user.email}


def get_user(db: Session = Depends(get_db), token: str = Depends(oauth_2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(Users).filter(Users.username == token_data.username).first()
    if user is None:
        raise credentials_exception

    return user
