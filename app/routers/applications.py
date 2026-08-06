from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session 

from app.database import get_db 
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate 

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)


@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
):
    application = Application(**application_data.model_dump())

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("/", response_model= list[ApplicationResponse])
def get_applications(
    db: Session = Depends(get_db),
): 
    statement = (
     select(Application)
     .order_by(Application.company_name)
     )
    
    result = db.execute(statement)
    return result.scalars().all()


@router.get("/{application_id}", response_model= ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
): 
    application = db.get(Application, application_id)
    
    if application is None: 
        raise HTTPException(
            status_code=404,
            detail="Application not found", 
        )
    return application


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)
    
    if application is None: 
            raise HTTPException(
                status_code=404,
                detail="Application not found", 
            )
    
    updates = application_data.model_dump(exclude_unset=True)
    
    for field, value in updates.items():
        setattr(application, field, value)
        
    db.commit()
    db.refresh(application)

    return application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    # Delete and save changes here
    db.delete(application)
    db.commit()
    return {"message": "Application deleted successfully"}