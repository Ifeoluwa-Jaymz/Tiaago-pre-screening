from pydantic import BaseModel

class JobDetails(BaseModel):
    job_title: str
    job_description: str
    num_questions: int
