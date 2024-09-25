from sqlalchemy import Column, String, Integer # type: ignore
from pydantic import BaseModel
from database import Base


class Notes(Base):

    __tablename__ = "notes"

    id = Column(Integer, primary_key= True)
    title = Column(String)
    description = Column(String)


class Users(Base):

    __tablename__ = "users"

    username = Column(String)
    email = Column(String, primary_key= True)
    hashed_password = Column(String)



class Token(BaseModel):

    access_token: str
    token_type: str | None = None


class TokenData(BaseModel):
    
    username: str | None = None



