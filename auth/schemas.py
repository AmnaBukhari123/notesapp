from pydantic import BaseModel

class Token(BaseModel):

    access_token: str
    token_type: str | None = None


class TokenData(BaseModel):
    
    username: str | None = None



class CreateUsers(BaseModel):
    username: str
    email: str
    password: str