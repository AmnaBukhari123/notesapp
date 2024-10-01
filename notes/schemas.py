from pydantic import BaseModel

class CreateNotes(BaseModel):
    title: str
    description: str


class NoteResponse(BaseModel):
    id: int
    title: str
    description: str
