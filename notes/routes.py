from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from notes.models import Notes
from notes.schemas import CreateNotes, NoteResponse
from database.service import get_db  # type: ignore
from auth.routes import get_user
from auth.models import Users
from notes.service import get_all_notes, create_note  # Import service functions


router = APIRouter()


@router.get("/notes", response_model=List[NoteResponse])
def read_notes(db: Session = Depends(get_db), current_user: Users = Depends(get_user)):
    notes = get_all_notes(db)  # Use service function to get notes
    return notes


@router.post("/notes", response_model=NoteResponse)
def write_notes(
    note: CreateNotes,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_user),
):
    db_note = create_note(db, note)  # Use service function to create note
    return db_note
