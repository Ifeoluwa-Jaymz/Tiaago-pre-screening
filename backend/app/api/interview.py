from fastapi import APIRouter
from app.models.schema import JobDetails

router = APIRouter()

@router.post("/start-interview")
def start_interview(job_details: JobDetails):
    return {"message": "Endpoint is placeholder for now."}
