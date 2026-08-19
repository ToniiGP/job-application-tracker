from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Interview, Application
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


def get_interviews(
    db: Session,
    application_id: int,
    user_id: int,
) -> list[Interview]:
    
    application = get_application(
        db,
        application_id,
        user_id,
    )

    if application is None:
        return []
    
    statement = select(Interview).where(
        Interview.application_id == application_id
    ) 
    
    result = db.execute(statement)
    return result.scalars().all()


def get_interview(
    db: Session,
    interview_id: int,
    user_id: int,
) -> Interview | None:
    
    statement = (select(Interview).join(
            Application,
            Interview.application_id == Application.id,
        )
        .where(
            Interview.id == interview_id,
            Application.user_id == user_id,
        )
    )
    
    result = db.execute(statement)
    return result.scalars().first()