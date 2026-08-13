from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session 
from app.services import user_service 

from app.database import get_db 
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin
from app.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db), 
): 
    
    try:
        return user_service.create_user(
            db, 
            user_data, 
        )
    
    except user_service.UserAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists.",
        )


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
    