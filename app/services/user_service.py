from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin
from app.security import hash_password

class UserAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("A user with this email already exists.")
        self.name = "UserAlreadyExistsError"


def get_user_by_email(
    db: Session, 
    email: str, 
) -> User | None: 
    
    statement = select(User)
    statement = statement.where(User.email == email)
    
    result = db.execute(statement)
    return result.scalars().first()


def create_user(
    db: Session, 
    user_data: UserCreate, 
) -> User: 
    
    existing_user = get_user_by_email(
    db,
    user_data.email,
    )

    if existing_user is not None:
        raise UserAlreadyExistsError()
    
    
    hashed_password = hash_password(user_data.password)

    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user 


