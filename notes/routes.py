from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from notes.models import Notes
from notes.schemas import CreateNotes, NoteResponse
from database.database import get_db # type: ignore
from auth.routes import get_user
from auth.models import Users
from typing import List

router = APIRouter()

@router.get("/read-notes", response_model=List[NoteResponse])
def read_notes(db: Session = Depends(get_db),  current_user: Users = Depends(get_user)):
    notes = db.query(Notes).all()
    return notes

@router.post("/write-notes", response_model=NoteResponse)
def write_notes(note: CreateNotes, db: Session = Depends(get_db),  current_user: Users = Depends(get_user)):
    db_note = Notes(title=note.title, description=note.description)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
