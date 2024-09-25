from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

db_URL = "postgresql://postgres:admin123@localhost/notesapp"

engine = create_engine(db_URL)

SessionLocal = sessionmaker(bind= engine)

Base = declarative_base()

Base.metadata.create_all(engine)

