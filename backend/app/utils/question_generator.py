import random

def generate_questions(job_title, job_description, num_questions, seed=None):
    if seed:
        random.seed(seed)  # Use the seed to ensure unique randomness
    # Example question templates
    base_questions = [
        f"Describe your experience with {job_title}.",
        f"What challenges have you faced in {job_title} roles?",
        f"How would you approach a task involving {job_description}?",
        "What is your biggest strength related to this role?",
        "How do you handle tight deadlines?",
    ]
    # Randomly sample questions
    return random.sample(base_questions, min(num_questions, len(base_questions)))
