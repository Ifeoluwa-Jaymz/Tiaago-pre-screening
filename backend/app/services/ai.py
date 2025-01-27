import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def evaluate_answer(question, answer):
    """
    Evaluate the user's answer using OpenAI GPT-4.

    Args:
        question (str): The interview question.
        answer (str): The user's answer.

    Returns:
        tuple: (grade (int), feedback (str)) - Grade out of 100 and detailed feedback.
    """
    prompt = (
        f"You are an expert recruiter grading a candidate's answer during a job interview.\n\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n\n"
        f"Provide a grade out of 100 and detailed feedback. "
        f"Focus on clarity, relevance, and depth of the answer. Return the result in this format:\n\n"
        f"Grade: <numeric grade between 0 and 100>\n"
        f"Feedback: <detailed feedback>"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in recruitment and evaluation."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.5,
        )
        # Extract grade and feedback from the response
        content = response["choices"][0]["message"]["content"]
        grade_line = [line for line in content.split("\n") if line.startswith("Grade:")][0]
        feedback_line = [line for line in content.split("\n") if line.startswith("Feedback:")][0]

        grade = int(grade_line.split(":")[1].strip())
        feedback = feedback_line.split(":", 1)[1].strip()

        return grade, feedback
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        # Fallback in case of API failure
        return 0, "Unable to evaluate the answer at the moment. Please try again later."
