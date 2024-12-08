from pydantic import BaseModel

class QuestionResponse(BaseModel):
    session_id: str
    answer: str

class NextQuestion(BaseModel):
    session_id: str
    question: str
