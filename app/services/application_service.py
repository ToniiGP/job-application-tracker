from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models import Application
from app.schemas import ApplicationCreate, ApplicationUpdate, ApplicationStatus

def create_application(
    db: Session,
    application_data: ApplicationCreate,
) -> Application:
    
    application = Application(**application_data.model_dump())
    
    db.add(application)
    db.commit()
    db.refresh(application)
    
    return application

def get_applications(
    db: Session,
    status: ApplicationStatus | None = None 
) -> list[Application]:
    
    statement = select(Application)

    if status is not None:
        statement = statement.where(
            Application.status == status
        )

    statement = statement.order_by(
        Application.company_name
    )

    result = db.execute(statement)
    return result.scalars().all()

def get_application(
    db: Session,
    application_id: int,
) -> Application | None:
    
    application = db.get(Application, application_id)
    return application

def delete_application(
    db: Session,
    application_id: int,
) -> bool:
    
    application = db.get(Application, application_id)
    
    if application is None:
        return False

    # Delete and save changes here
    db.delete(application)
    db.commit()
    return True #application deleted succesfuly 

def update_application(
    db: Session,
    application_id: int,
    application_data: ApplicationUpdate,
) -> Application | None:

    application = db.get(Application, application_id)

    if application is None:
        return None

    updates = application_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application