from datetime import date, datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SQLEnum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ApplicationStatus(str, Enum):
    WISHLIST = "Wishlist"
    APPLIED = "Applied"
    ONLINE_ASSESSMENT = "Online Assessment"
    PHONE_SCREEN = "Phone Screen"
    TECHNICAL_INTERVIEW = "Technical Interview"
    FINAL_INTERVIEW = "Final Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(100), nullable=False)
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(
        SQLEnum(ApplicationStatus),
        default=ApplicationStatus.WISHLIST,
        nullable=False,
    )
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    job_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    date_applied: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
class User(Base): 
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )