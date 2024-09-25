from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends, status
from models import Notes, Users, TokenData, Token
from passlib.context import CryptContext # type: ignore
from jose  import JWTError, jwt # type: ignore
from database import engine, SessionLocal
from datetime import timedelta
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List


SECRET_KEY = "7576a5fb4dec953d694206811b7ed1d87f16953a52f6093541e6d7a7bbbb1b7b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#this string is used to hash passwords and defines the scheme to be used
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#compares both passwords' hashes
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def  get_password_hash(password):
    return pwd_context.hash(password)

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


    
def authenticate_user(db, username: str, password: str):

    user = db.query(Users).filter(Users.username == username).first() 

    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user



app = FastAPI()


class CreateNotes(BaseModel):
    title: str
    description: str


class NoteResponse(BaseModel):
    id: int
    title: str
    description: str


class CreateUsers(BaseModel):
    username: str
    email: str
    password: str


@app.post("/token", response_model=Token)
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



@app.get("/read-notes", response_model=List[NoteResponse])
def read_notes(db: Session = Depends(get_db),  current_user: Users = Depends(get_user)):
    notes = db.query(Notes).all()
    return notes

@app.post("/write-notes", response_model=NoteResponse)
def write_notes(note: CreateNotes, db: Session = Depends(get_db),  current_user: Users = Depends(get_user)):
    db_note = Notes(title=note.title, description=note.description)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.post("/registers")
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


