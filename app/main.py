from fastapi import FastAPI

from app.database import test_database_connection

app = FastAPI(
    title="Job Application Tracker API",
    description="API for managing job applications.",
    version="0.1.0",
)

@app.get("/")
def read_root() -> dict[str, str]: 
    return {"message": "Job Application Tracker API is running"}

@app.get("/database-test")
def database_test():
    test_database_connection()
    return {"message": "Database connection successful"}