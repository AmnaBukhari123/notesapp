from sqlalchemy.orm import Session
from auth.models import Users
from auth.schemas import CreateUsers
from auth.utils import get_password_hash

class UserService:
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        """Fetch user by username."""
        return db.query(Users).filter(Users.username == username).first()

    @staticmethod
    def user_exists(db: Session, username: str, email: str):
        """Check if a user with the given username or email exists."""
        return db.query(Users).filter(
            (Users.username == username) | (Users.email == email)
        ).first()

    @staticmethod
    def create_user(db: Session, user: CreateUsers):
        """Create a new user."""
        hashed_password = get_password_hash(user.password)
        new_user = Users(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
