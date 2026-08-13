from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session 
from app.services import application_service

from app.database import get_db 
from app.models import Application, User
from app.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate, ApplicationStatus
from app.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)


@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return application_service.create_application(
        db,
        application_data,
        current_user.id,
    )


@router.get("/", response_model= list[ApplicationResponse])
def get_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status: ApplicationStatus | None = None,
    company: str | None = None,
    job_title: str | None = None, 
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
): 
   return application_service.get_applications(db, current_user.id, status=status, company=company, job_title=job_title, page=page, page_size=page_size)


@router.get("/{application_id}", response_model= ApplicationResponse)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
): 
    application = application_service.get_application(
        db,
        application_id,
        current_user.id,
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = application_service.update_application(
        db,
        application_id,
        current_user.id,
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = application_service.delete_application(
        db,
        application_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return {"message": "Application deleted successfully"}