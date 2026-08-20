from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from app.services import interview_service
from app.models import User

from app.database import get_db 
from app.schemas import InterviewCreate, InterviewResponse, InterviewUpdate
from app.auth_dependencies import get_current_user

router = APIRouter(
    tags=["interviews"],
)

@router.post(
    "/applications/{application_id}/interviews",
    response_model=InterviewResponse,
    status_code=201,
)
def create_interview(
    application_id: int,
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = interview_service.create_interview(
        db, 
        application_id, 
        current_user.id, 
        interview_data,
    )
    
    if interview is None: 
        raise HTTPException(
            status_code=404,
            detail="Interview not found",
        )
        
    return interview 

@router.get(
    "/applications/{application_id}/interviews", 
    response_model=list[InterviewResponse],
)
def get_interviews(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db), 
): 
    return interview_service.get_interviews(db, application_id, current_user.id)

@router.get(
    "/interviews/{interview_id}",
    response_model=InterviewResponse,
)
def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
): 
    interview = interview_service.get_interview(db, interview_id, current_user.id)
    
    if interview is None: 
            raise HTTPException(
                status_code=404,
                detail="Interview not found",
            )
            
    return interview 

@router.patch(
    "/interviews/{interview_id}", 
    response_model= InterviewResponse,
)
def update_interview(
    interview_id: int,
    interview_data: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
): 
    
    interview = interview_service.update_interview(
        db,
        interview_id, 
        current_user.id,
        interview_data,
    )
    
    if interview is None: 
            raise HTTPException(
                status_code=404,
                detail="Application not found",
            )
                
    return interview 
    
    
@router.delete("/interviews/{interview_id}")
def delete_interview(
    interview_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    deleted = interview_service.delete_interview(
        db, 
        interview_id, 
        current_user.id,
    )
    
    if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Interview not found",
            )
    
    return {"message": "Interview deleted successfully"}
