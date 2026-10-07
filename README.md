# 🧠 LearnLoop AI
**Understand it. Connect it. Apply it.**

LearnLoop AI helps students move beyond memorization by explaining topics simply, showing relationships between concepts, and generating practice quizzes.

## Features
- **Explain My Topic:** simple explanation, importance, real-world example, key takeaway.
- **Connect the Concepts:** related concepts, relationships, and analogy.
- **Learn by Applying:** multiple-choice practice quiz with answer key and explanations.
- Personalized level and language options.
- Groq API key is entered locally; never commit secrets.

## Tech stack
Python · Streamlit · Groq API

## Run locally
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. In the terminal, run `python -m venv .venv`.
4. Activate it: PowerShell: `.venv\\Scripts\\Activate.ps1`; Git Bash: `source .venv/Scripts/activate`.
5. Install: `pip install -r requirements.txt`.
6. Copy `.env.example` to `.env` and add your Groq API key, or paste the key into the app sidebar.
7. Run `streamlit run app.py`.

Get a key at https://console.groq.com/. Never publish your API key or commit `.env`.

## Deploy
Push this repository to GitHub, then deploy through Streamlit Community Cloud. Set `GROQ_API_KEY` in the app's Secrets settings.

## Hackathon readiness
Test all features, take original screenshots, publish a 2–4 minute demo video, and document the work completed during the event. AI-generated content can be incorrect; verify important facts.
