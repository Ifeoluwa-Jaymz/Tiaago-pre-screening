import streamlit as st
import uuid
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.questions import generate_questions
from services.ai import evaluate_answer

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None
    st.session_state["name"] = None
    st.session_state["job_title"] = None
    st.session_state["job_description"] = None
    st.session_state["questions"] = []
    st.session_state["answers"] = []
    st.session_state["current_question_index"] = 0
    st.session_state["finished"] = False
    st.session_state["step"] = "name_input"  # Current step in the flow
    st.session_state["transcript"] = []
    st.session_state["total_grade"] = 0


# Helper function to move to the next step
def move_to_next_step(step_name):
    st.session_state["step"] = step_name


# App flow based on steps
st.title("AI Pre-Screening Interview System")

if st.session_state["step"] == "name_input":
    st.header("Welcome!")
    name = st.text_input("What's your first name?")
    if name:
        st.session_state["name"] = name
        if st.session_state["session_id"] is None:
            # Generate session ID using the name and a UUID
            st.session_state["session_id"] = f"{name.lower()}_{uuid.uuid4().hex[:6]}"
        st.success(f"Hi {name}! Your session ID is **{st.session_state['session_id']}**. Let's get started.")
        if st.button("Next"):
            move_to_next_step("confirmation")

elif st.session_state["step"] == "confirmation":
    st.header("Confirmation")
    st.write(f"Hello, **{st.session_state['name']}**!")
    st.write("Do you want to proceed with the interview?")
    user_response = st.radio("Select an option:", ["Yes", "No"])

    if st.button("Submit"):
        if user_response == "Yes":
            st.success("Great! Proceeding to the interview setup.")
            move_to_next_step("job_details")
        elif user_response == "No":
            st.warning("You have chosen to end the interview. Thank you!")
            st.stop()  # End the app execution

elif st.session_state["step"] == "job_details":
    st.subheader("Enter Job Details")
    job_title = st.text_input("Enter the job title:")
    job_description = st.text_area("Enter the job description:")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=5)

    if st.button("Generate Questions"):
        if job_title and job_description:
            st.session_state["job_title"] = job_title
            st.session_state["job_description"] = job_description

            # Generate questions using OpenAI
            questions = generate_questions(job_title, job_description, num_questions)

            if questions:
                st.session_state["questions"] = questions[:num_questions]  # Respect the requested number of questions
                st.success("Questions successfully generated! Let's begin.")
                move_to_next_step("interview")
            else:
                st.error("Failed to generate questions. Please try again.")
        else:
            st.error("Please provide both job title and job description.")

elif st.session_state["step"] == "interview":
    # Question and answer flow
    current_index = st.session_state["current_question_index"]
    questions = st.session_state["questions"]

    if current_index < len(questions):
        question = questions[current_index]
        st.write(f"**Question {current_index + 1}:** {question}")
        answer = st.text_area("Your Answer", key=f"answer_{current_index}")

        if st.button("Submit Answer", key=f"submit_{current_index}"):
            if answer.strip():
                # Pass both the question and the answer to evaluate_answer
                grade, feedback = evaluate_answer(question, answer)

                # Store the question, answer, grade, and feedback
                st.session_state["answers"].append({
                    "question": question,
                    "answer": answer,
                    "grade": grade,
                    "feedback": feedback,
                })
                st.session_state["current_question_index"] += 1
                if st.session_state["current_question_index"] >= len(questions):
                    move_to_next_step("summary")
            else:
                st.error("Please provide an answer before submitting.")
    else:
        st.warning("No more questions. Moving to the summary.")
        move_to_next_step("summary")

elif st.session_state["step"] == "summary":
    st.header("Interview Summary")
    st.write(f"**Session ID:** {st.session_state['session_id']}")

    # Display the answers and feedback
    transcript = st.session_state["answers"]
    total_grade = sum(answer["grade"] for answer in transcript)
    average_score = total_grade / len(transcript)

    st.write(f"**Total Score:** {total_grade} / {len(transcript) * 100} "
             f"(**{average_score:.2f}% Average**)")

    # Display detailed transcript
    st.subheader("Transcript")
    for idx, entry in enumerate(transcript, start=1):
        st.write(f"**Q{idx}:** {entry['question']}")
        st.write(f"**A:** {entry['answer']}")
        st.write(f"**Grade:** {entry['grade']} / 100")
        st.write(f"**Feedback:** {entry['feedback']}")
        st.write("---")

    # Add a restart button
    if st.button("Restart"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
