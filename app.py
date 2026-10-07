import json
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="LearnLoop AI",
    page_icon="🧠",
    layout="wide"
)


# -----------------------------
# App styling
# -----------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2rem;
        border-radius: 24px;
        background: linear-gradient(120deg, #182848, #4b6cb7);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: white !important;
        font-size: 2.7rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #e8eeff !important;
        font-size: 1.1rem;
    }

    /* Make normal text follow the selected Streamlit theme */
    .stMarkdown,
    .stText,
    label,
    p {
        color: var(--text-color);
    }

    /* Input fields */
    .stTextInput input {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
    }

    /* Select boxes */
    [data-baseweb="select"] {
        background-color: var(--secondary-background-color);
    }

    /* Keep tabs readable in both themes */
    button[data-baseweb="tab"] {
        color: var(--text-color);
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 1rem;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Session state
# -----------------------------

if "quiz_data" not in st.session_state:
    st.session_state["quiz_data"] = None

if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = {}

if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False

if "quiz_history" not in st.session_state:
    st.session_state["quiz_history"] = []


# -----------------------------
# Hero section
# -----------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🧠 LearnLoop AI</h1>
        <p>Understand it. Connect it. Apply it.</p>
        Personal AI tutor · Concept connections · Practice quizzes
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Learning setup
# -----------------------------

with st.sidebar:
    st.header("Learning setup")

    level = st.selectbox(
        "Your level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    language = st.selectbox(
        "Explanation language",
        ["Simple English", "Bangla", "English + Bangla"]
    )

    manual_key = st.text_input(
        "Groq API key",
        type="password"
    )

    st.caption(
        "You can add your Groq key here, or keep it in the .env file."
    )

    # Learning progress
    st.divider()
    st.subheader("📊 Learning Progress")

    history = st.session_state["quiz_history"]

    if history:
        total_quizzes = len(history)

        total_score = sum(
            item["score"] for item in history
        )

        total_questions = sum(
            item["total"] for item in history
        )

        average_score = (
            total_score / total_questions * 100
            if total_questions
            else 0
        )

        st.metric(
            "Quizzes completed",
            total_quizzes
        )

        st.metric(
            "Average score",
            f"{average_score:.0f}%"
        )

    else:
        st.caption(
            "Complete a quiz to see your progress."
        )


# -----------------------------
# AI setup
# -----------------------------

api_key = manual_key.strip() or os.getenv("GROQ_API_KEY")

model = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)


def ask_ai(prompt):
    """Send a prompt to Groq and return the response."""

    if not api_key:
        st.error(
            "Groq API key not found. Add it in the sidebar "
            "or set GROQ_API_KEY in your .env file."
        )
        return None

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are LearnLoop AI, a friendly and patient tutor. "
                        "Explain things clearly and naturally. "
                        "Keep answers useful and practical. "
                        "If you are unsure about something, say so."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(
            f"Something went wrong while talking to the AI: {e}"
        )
        return None


# -----------------------------
# Topic input
# -----------------------------

st.subheader("What would you like to learn today?")

topic = st.text_input(
    "Enter a topic",
    placeholder="e.g. Neural networks, photosynthesis, probability"
)


# -----------------------------
# Main tabs
# -----------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📘 Explain",
        "🔗 Connect concepts",
        "🎯 Practice quiz"
    ]
)


# =========================================================
# TAB 1 — EXPLAIN
# =========================================================

with tab1:
    st.subheader("Explain My Topic")

    st.write(
        "Learn a difficult topic in a way that matches your level."
    )

    if st.button(
        "Explain topic",
        type="primary",
        use_container_width=True
    ):
        if not topic.strip():
            st.warning("Please enter a topic first.")

        else:
            prompt = f"""
You are teaching a student through LearnLoop AI.

Topic: {topic}
Student level: {level}
Preferred language: {language}

Explain the topic like a good human tutor.

Use these sections:

## 1. In simple words
Explain the main idea using simple language.

## 2. Why it matters
Explain why learning this topic is useful.

## 3. Real-life example
Give one simple example from everyday life,
education, or technology.

## 4. Key points
Give 3 to 5 important points to remember.

## 5. Common mistake
Mention one common misunderstanding students may have.

## 6. Quick check
Ask one short question to check the student's understanding.
Do not give the answer yet.

If the topic contains a difficult technical term,
explain that term before using it.
"""

            with st.spinner(
                "Your tutor is preparing the explanation..."
            ):
                result = ask_ai(prompt)

            if result:
                st.markdown(result)

                st.success(
                    "Try answering the Quick Check before moving on."
                )


# =========================================================
# TAB 2 — CONNECT CONCEPTS
# =========================================================

with tab2:
    st.subheader("Connect the Concepts")

    st.write(
        "See how the main topic connects with other ideas."
    )

    if st.button(
        "Build concept connections",
        type="primary",
        use_container_width=True
    ):
        if not topic.strip():
            st.warning("Please enter a topic first.")

        else:
            prompt = f"""
Create a simple concept connection guide for:

Topic: {topic}
Student level: {level}
Language: {language}

Include:

1. The central concept
2. Five related concepts
3. Four relationships using this format:
   "A connects to B because..."
4. One easy analogy that helps the student
   understand the connection.

Keep the explanation practical and easy to understand.
Avoid unnecessary technical language.
"""

            with st.spinner("Connecting ideas..."):
                result = ask_ai(prompt)

            if result:
                st.markdown(result)


# =========================================================
# TAB 3 — INTERACTIVE QUIZ
# =========================================================

with tab3:
    st.subheader("Learn by Applying")

    st.write(
        "Test what you know with a short interactive quiz."
    )

    count = st.select_slider(
        "Number of questions",
        options=[3, 5, 7],
        value=5
    )

    if st.button(
        "Generate quiz",
        type="primary",
        use_container_width=True
    ):
        if not topic.strip():
            st.warning("Please enter a topic first.")

        else:
            prompt = f"""
Create a multiple-choice quiz for a student.

Topic: {topic}
Student level: {level}
Language: {language}
Number of questions: {count}

Return ONLY valid JSON in this exact structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": 0,
            "explanation": "Short explanation of the correct answer."
        }}
    ]
}}

Rules:

- "answer" must be 0, 1, 2, or 3.
- 0 means the first option.
- 1 means the second option.
- 2 means the third option.
- 3 means the fourth option.
- Create exactly {count} questions.
- Only one option should be correct.
- Keep questions clear and relevant.
- Do not use markdown.
- Do not add text outside the JSON.
"""

            with st.spinner("Creating your quiz..."):
                result = ask_ai(prompt)

            if result:
                try:
                    clean_result = result.strip()

                    if clean_result.startswith("```"):
                        clean_result = (
                            clean_result
                            .replace("```json", "")
                            .replace("```", "")
                            .strip()
                        )

                    quiz_data = json.loads(clean_result)

                    st.session_state["quiz_data"] = quiz_data
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_submitted"] = False

                except json.JSONDecodeError:
                    st.error(
                        "The AI returned an invalid quiz format. "
                        "Please generate the quiz again."
                    )

    quiz_data = st.session_state["quiz_data"]

    if quiz_data:
        questions = quiz_data.get("questions", [])

        st.divider()
        st.subheader("📝 Your Quiz")

        for index, question in enumerate(questions):
            st.markdown(
                f"### Question {index + 1}"
            )

            st.write(question["question"])

            answer = st.radio(
                "Choose one:",
                question["options"],
                key=f"quiz_question_{index}",
                index=None
            )

            st.session_state["quiz_answers"][index] = answer

        st.write("")

        if st.button(
            "Submit Quiz",
            type="primary",
            use_container_width=True
        ):
            score = 0

            for index, question in enumerate(questions):
                selected_answer = (
                    st.session_state["quiz_answers"].get(index)
                )

                correct_index = question["answer"]

                if (
                    selected_answer is not None
                    and selected_answer
                    == question["options"][correct_index]
                ):
                    score += 1

            total = len(questions)

            # Save quiz result
            st.session_state["quiz_history"].append(
                {
                    "topic": topic,
                    "score": score,
                    "total": total
                }
            )

            st.session_state["last_score"] = score
            st.session_state["last_total"] = total
            st.session_state["quiz_submitted"] = True

        if st.session_state["quiz_submitted"]:
            score = st.session_state["last_score"]
            total = st.session_state["last_total"]

            st.divider()

            if score == total:
                st.success(
                    f"🎉 Excellent! You scored {score}/{total}."
                )

            elif score >= total * 0.6:
                st.info(
                    f"👍 Good job! You scored {score}/{total}."
                )

            else:
                st.warning(
                    f"Keep practicing! You scored {score}/{total}."
                )

            st.subheader("📊 Your Results")

            for index, question in enumerate(questions):
                selected_answer = (
                    st.session_state["quiz_answers"].get(index)
                )

                correct_index = question["answer"]
                correct_answer = question["options"][correct_index]

                if selected_answer == correct_answer:
                    st.success(
                        f"Question {index + 1}: Correct ✅"
                    )

                else:
                    st.error(
                        f"Question {index + 1}: Incorrect ❌"
                    )

                    if selected_answer is None:
                        st.write(
                            "You did not select an answer."
                        )
                    else:
                        st.write(
                            f"Your answer: {selected_answer}"
                        )

                    st.write(
                        f"Correct answer: {correct_answer}"
                    )

                st.caption(
                    f"Explanation: {question['explanation']}"
                )


# =========================================================
# AI STUDY SUGGESTION
# =========================================================

if st.session_state["quiz_history"]:
    st.divider()

    st.subheader("🧠 AI Study Suggestion")

    if st.button(
        "Suggest what I should study next",
        use_container_width=True
    ):
        history = st.session_state["quiz_history"]

        history_text = "\n".join(
            [
                f"Topic: {item['topic']}, "
                f"Score: {item['score']}/{item['total']}"
                for item in history
            ]
        )

        prompt = f"""
You are a personal AI tutor.

Recent quiz history:

{history_text}

Based on this performance:

1. Identify the topic where the student needs
   the most improvement.
2. Explain briefly why.
3. Suggest what they should study next.
4. Give one practical study tip.

Keep the response short, friendly and useful.

Use this language:
{language}
"""

        with st.spinner(
            "Analyzing your learning progress..."
        ):
            suggestion = ask_ai(prompt)

        if suggestion:
            st.markdown(suggestion)


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.markdown(
    """
    <p style='text-align:center;color:#68738a'>
        LearnLoop AI · Learn. Connect. Apply. · ForgeHacks
    </p>
    """,
    unsafe_allow_html=True
)