import openai
import os
from dotenv import load_dotenv

# Load the OpenAI API key from the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_question(previous_questions: list, role: str = "Software Engineer"):
    """
    Generate a new interview question using OpenAI based on the role and previous questions.
    """
    try:
        prompt = (
            f"You are an expert interviewer designing questions for a {role} position. "
            f"The following questions have already been asked: {', '.join(previous_questions)}. "
            "Generate one new and engaging interview question that evaluates the candidate's technical skills, cultural fit, or problem-solving abilities."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        question = response['choices'][0]['message']['content'].strip()
        return question
    except Exception as e:
        print(f"Error generating question: {e}")
        return "What inspired you to pursue this role?"
