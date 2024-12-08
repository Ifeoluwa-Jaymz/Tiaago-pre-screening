from fastapi import FastAPI
from app.api import interview

app = FastAPI()

# Include the interview routes
app.include_router(interview.router)

@app.get("/")
def root():
    return {"message": "AI Pre-Screening Interview System"}
