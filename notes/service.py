from sqlalchemy.orm import Session
from notes.models import Notes
from notes.schemas import CreateNotes


def get_all_notes(db: Session):
    """Fetch all notes from the database."""
    return db.query(Notes).all()


def create_note(db: Session, note: CreateNotes):
    """Create a new note and save it to the database."""
    db_note = Notes(title=note.title, description=note.description)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
