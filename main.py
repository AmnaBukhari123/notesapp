from fastapi import FastAPI
from database.service import Base, engine
from auth.routes import router as auth_router
from notes.routes import router as notes_router


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(auth_router, prefix="/auth")
app.include_router(notes_router, prefix="/notes")