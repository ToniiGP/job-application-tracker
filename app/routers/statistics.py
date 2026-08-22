from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from app.services import statistics_service
from app.models import User

from app.database import get_db 
from app.schemas import StatisticsSummary
from app.auth_dependencies import get_current_user

router = APIRouter(
    tags=["Statistics"],
)

@router.get("/statistics/summary", response_model=StatisticsSummary,)
def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
): 
    
    return statistics_service.get_statistics_summary(db, current_user.id)
