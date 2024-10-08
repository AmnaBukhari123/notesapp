from sqlalchemy import Column, String, Integer  # type: ignore
from database.service import Base


class Notes(Base):

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
