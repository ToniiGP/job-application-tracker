from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Interview
from app.schemas import InterviewCreate
from services.application_service import get_application

def create_interview(
    db: Session, 
    application_id: int, 
    user_id: int, 
    interview_data: InterviewCreate 
) -> Interview | None: 
    
    application = get_application(
        db,
        application_id,
        user_id,
    )

    if application is None:
        return None 
    
    interview = Interview(
        application_id=application_id,
        **interview_data.model_dump(),
    )
    
    db.add(interview)
    db.commit()
    db.refresh(interview)
    
    return interview 