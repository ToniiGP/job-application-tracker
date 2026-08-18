from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models import Application
from app.schemas import ApplicationCreate, ApplicationUpdate, ApplicationStatus


def create_application(
    db: Session,
    application_data: ApplicationCreate,
    user_id: int,
) -> Application:
    
    application = Application(
        **application_data.model_dump(),
        user_id=user_id,
        )
    
    db.add(application)
    db.commit()
    db.refresh(application)
    
    return application

def get_applications(
    db: Session,
    user_id: int,
    status: ApplicationStatus | None = None,
    company: str | None = None, 
    job_title: str | None = None,
    page: int = 1, 
    page_size: int = 20, 
) -> list[Application]:
    
    statement = select(Application).where(
    Application.user_id == user_id
    )

    if status is not None:
        statement = statement.where(
            Application.status == status
        )
    
    if company is not None:
        statement = statement.where(
        Application.company_name.ilike(f"%{company}%")
    )
        
    if job_title is not None: 
        statement = statement.where(
            Application.job_title.ilike(f"%{job_title}%")
        )

    statement = statement.order_by(
        Application.company_name
    )
    
    offset = (page - 1) * page_size

    statement = statement.offset(offset).limit(page_size)


    result = db.execute(statement)
    return result.scalars().all()

def get_application(
    db: Session,
    application_id: int,
    user_id: int, 
) -> Application | None:
    
    statement = select(Application).where(
    Application.id == application_id,
    Application.user_id == user_id,
    )

    result = db.execute(statement)

    return result.scalars().first()


def delete_application(
    db: Session,
    application_id: int,
    user_id: int, 
) -> bool:
    
    statement = select(Application).where(
    Application.id == application_id,
    Application.user_id == user_id,
    )

    result = db.execute(statement)
    application = result.scalars().first()
    
    if application is None:
        return False

    # Delete and save changes here
    db.delete(application)
    db.commit()
    return True #application deleted succesfuly 

def update_application(
    db: Session,
    application_id: int,
    user_id: int,
    application_data: ApplicationUpdate,
) -> Application | None:

    statement = select(Application).where(
    Application.id == application_id,
    Application.user_id == user_id,
)

    result = db.execute(statement)
    application = result.scalars().first()

    if application is None:
        return None

    updates = application_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application