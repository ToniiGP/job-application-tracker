from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session 
from app.services import user_service 

from app.database import get_db 
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin
