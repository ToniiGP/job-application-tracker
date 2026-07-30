from datetime import date, datetime 

from pydantic import BaseModel, ConfigDict

from app.models import ApplicationStatus


class ApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    status: ApplicationStatus
    location: str | None = None
    job_url: str | None = None
    date_applied: date | None = None
    notes: str | None = None
    

class ApplicationResponse(BaseModel): 
    id: int 
    company_name: str
    job_title: str
    status: ApplicationStatus
    location: str | None
    job_url: str | None
    date_applied: date | None
    notes: str | None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True) 
    