from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 

from app.database import get_db 
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationResponse

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

