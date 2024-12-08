from app.services.ai import generate_question

def get_next_question(asked_questions, role="Software Engineer"):
    """
    Uses OpenAI to generate the next question dynamically.
    """
    return generate_question(asked_questions, role)
