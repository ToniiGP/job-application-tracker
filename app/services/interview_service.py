from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Interview, Application
from app.schemas import InterviewCreate, InterviewUpdate
from app.services.application_service import get_application

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
) -> list[Interview] | None:
    
    application = get_application(
        db,
        application_id,
        user_id,
    )

    if application is None:
        return None
    
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


def update_interview(
    db: Session,
    interview_id: int,
    user_id: int,
    interview_data: InterviewUpdate,
) -> Interview | None:

    interview = get_interview(
        db,
        interview_id,
        user_id,
    )

    if interview is None:
        return None

    updates = interview_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(interview, field, value)

    db.commit()
    db.refresh(interview)

    return interview


def delete_interview(
    db: Session,
    interview_id: int,
    user_id: int,
) -> bool:

    interview = get_interview(
        db,
        interview_id,
        user_id,
    )

    if interview is None:
        return False

    db.delete(interview)
    db.commit()

    return True