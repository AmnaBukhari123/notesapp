from sqlalchemy import Column, String, Integer  # type: ignore

from database.service import Base


class Users(Base):

    __tablename__ = "users"

    username = Column(String)
    email = Column(String, primary_key=True)
    hashed_password = Column(String)
