from datetime import date, datetime 

from pydantic import BaseModel, ConfigDict

from app.models import ApplicationStatus, InterviewStage


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


class ApplicationUpdate(BaseModel): 
    company_name: str | None = None 
    job_title: str | None = None 
    status: ApplicationStatus | None = None 
    location: str | None = None 
    job_url: str | None = None
    date_applied: date | None = None 
    notes: str | None = None 
    
class UserCreate(BaseModel): 
    email: str 
    username: str 
    password: str 
    

class UserResponse(BaseModel): 
    id: int 
    email: str 
    username: str 
    created_at: datetime
    
class UserLogin(BaseModel): 
    email: str 
    password: str 

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class InterviewCreate(BaseModel): 
    stage: InterviewStage
    scheduled_at: datetime | None = None 
    interviewer: str | None = None 
    notes: str | None = None 

class InterviewResponse(BaseModel): 
    id: int 
    application_id: int
    stage: InterviewStage
    scheduled_at: datetime | None = None 
    interviewer: str | None = None 
    notes: str | None = None
    created_at: datetime

class InterviewUpdate(BaseModel): 
    stage: InterviewStage | None = None
    scheduled_at: datetime | None = None 
    interviewer: str | None = None 
    notes: str | None = None 