from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session 
from app.services import application_service

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
    return application_service.create_application(
        db,
        application_data,
    )


@router.get("/", response_model= list[ApplicationResponse])
def get_applications(
    db: Session = Depends(get_db),
): 
   return application_service.get_applications(db)


@router.get("/{application_id}", response_model= ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
): 
    application = application_service.get_application(
        db,
        application_id,
    )

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
    application = application_service.update_application(
        db,
        application_id,
        application_data,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    deleted = application_service.delete_application(
        db,
        application_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return {"message": "Application deleted successfully"}