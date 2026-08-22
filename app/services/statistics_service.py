from sqlalchemy.orm import Session

from app.schemas import StatisticsSummary
from sqlalchemy import func, select
from app.models import Application, ApplicationStatus, Interview


def get_statistics_summary(
    db: Session,
    user_id: int,
) -> StatisticsSummary:
    
    statement = (
    select(
        Application.status,
        func.count(Application.id),
    )
    .where(
        Application.user_id == user_id
    )
    .group_by(Application.status)
    )

    result = db.execute(statement)
    status_counts = result.all()

    counts = {
        status: count
        for status, count in status_counts
    }
    
    total_applications = sum(counts.values())
    
    wishlist = counts.get(ApplicationStatus.WISHLIST, 0)
    applied = counts.get(ApplicationStatus.APPLIED, 0)
    interviewing = (
        counts.get(ApplicationStatus.PHONE_SCREEN, 0)
        + counts.get(ApplicationStatus.TECHNICAL_INTERVIEW, 0)
        + counts.get(ApplicationStatus.FINAL_INTERVIEW, 0)
    )
    offers = counts.get(ApplicationStatus.OFFER, 0)
    rejected = counts.get(ApplicationStatus.REJECTED, 0)
    
    interview_statement = (
        select(func.count(Interview.id))
        .join(
            Application,
                Interview.application_id == Application.id,
        )
        .where(
            Application.user_id == user_id
        )
    )

    interview_result = db.execute(interview_statement)

    total_interviews = interview_result.scalar_one()
    
    return StatisticsSummary(
        total_applications=total_applications,
        wishlist=wishlist,
        applied=applied,
        interviewing=interviewing,
        offers=offers,
        rejected=rejected,
        total_interviews=total_interviews,
    )