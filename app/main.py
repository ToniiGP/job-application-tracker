from fastapi import FastAPI
from app.database import test_database_connection
import app.models
from app.database import create_database
from app.routers.applications import router as applications_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.interviews import router as interviews_router

app = FastAPI(
    title="Job Application Tracker API",
    description="API for managing job applications.",
    version="0.1.0",
)

create_database()

app.include_router(applications_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(interviews_router)

@app.get("/")
def read_root() -> dict[str, str]: 
    return {"message": "Job Application Tracker API is running"}

@app.get("/database-test")
def database_test():
    test_database_connection()
    return {"message": "Database connection successful"}