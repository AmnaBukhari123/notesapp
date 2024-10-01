from sqlalchemy import Column, String, Integer # type: ignore
from database.database import Base

class Users(Base):

    __tablename__ = "users"

    username = Column(String)
    email = Column(String, primary_key= True)
    hashed_password = Column(String)