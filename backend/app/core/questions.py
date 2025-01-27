import openai
import os
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_questions(job_title, job_description, num_questions):
    """
    Generate conversational questions using OpenAI GPT-4.
    
    Args:
        job_title (str): The job title.
        job_description (str): A detailed description of the job.
        num_questions (int): The number of questions to generate.
    
    Returns:
        List[str]: A list of conversational questions.
    """
    prompt = (
        f"You are an expert recruiter designing conversational interview questions for the job "
        f"of '{job_title}'. The job description is as follows:\n\n"
        f"{job_description}\n\n"
        f"Create {num_questions} interview questions that are friendly, conversational, and designed to assess both "
        f"the candidate's technical skills and cultural fit. Each question should be conversational, "
        f"starting with phrases like 'Can you tell me about...' or 'I'd love to hear your thoughts on...'."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in recruitment."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        # Extract questions from the response
        questions = response["choices"][0]["message"]["content"].strip().split("\n")
        return [q.strip() for q in questions if q.strip()]
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []
