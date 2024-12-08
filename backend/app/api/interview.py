from fastapi import APIRouter, HTTPException
from app.core.questions import get_next_question
from app.services.ai import process_response
from app.models.schemas import QuestionResponse, NextQuestion

router = APIRouter()

# Mock session data
SESSIONS = {}

@router.post("/start-interview/", response_model=NextQuestion)
async def start_interview(candidate_id: int, role: str = "Software Engineer"):
    """
    Start an AI-driven interview session.
    """
    session_id = f"session_{candidate_id}"
    SESSIONS[session_id] = {"questions_asked": [], "responses": [], "role": role}
    question = get_next_question(SESSIONS[session_id]["questions_asked"], role)
    SESSIONS[session_id]["questions_asked"].append(question)
    return {"session_id": session_id, "question": question}

@router.post("/answer-question/", response_model=NextQuestion)
async def answer_question(response: QuestionResponse):
    """
    Process the candidate's answer and provide the next question.
    """
    session_data = SESSIONS.get(response.session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    # Store the response
    session_data["responses"].append(response.answer)

    # Process the response (mock AI analysis)
    process_response(response.answer)

    # Get the next question
    next_question = get_next_question(session_data["questions_asked"], session_data["role"])
    if next_question:
        session_data["questions_asked"].append(next_question)
        return {"session_id": response.session_id, "question": next_question}
    else:
        return {"session_id": response.session_id, "question": "Interview completed"}
