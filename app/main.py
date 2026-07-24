from fastapi import FastAPI

app = FastAPI(
    title="Job Application Tracker API",
    description="API for managing job applications.",
    version="0.1.0",
)

@app.get("/")
def read_root() -> dict[str, str]: 
    return {"message": "Job Application Tracker API is running"}