from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.schemas import CreateUsers, Token, TokenData
from auth.utils import verify_password, get_password_hash
from auth.models import Users
from database.database import get_db 
from jose import jwt, JWTError
from datetime import timedelta 

# Import these from wherever they are defined
from auth.utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

    
def authenticate_user(db, username: str, password: str):

    user = db.query(Users).filter(Users.username == username).first() 

    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/registers")
def register_user(user: CreateUsers, db: Session = Depends(get_db)):
    # checking if the username or email already exists or not
    existing_user = db.query(Users).filter((Users.username == user.username) | (Users.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    # hashing the password here
    hashed_password = get_password_hash(user.password)

    #creating new user here
    new_user = Users(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "email": new_user.email}


def get_user(db: Session = Depends(get_db), token : str = Depends(oauth_2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username= username)

    except JWTError:
        raise credentials_exception

    user = db.query(Users).filter(Users.username == username).first() 

    if user is None:
        raise credentials_exception
    
    return user

