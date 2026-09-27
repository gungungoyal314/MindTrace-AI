import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google import genai


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(PROJECT_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add it to the .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# DIGITAL TWIN FILES
# ============================================================

PROFILE_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "attention_profile.csv"
)

BEHAVIOR_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "attention_behavior.csv"
)


# ============================================================
# LOAD DIGITAL TWIN
# ============================================================

def load_digital_twin():

    if not PROFILE_FILE.exists():

        raise FileNotFoundError(
            "attention_profile.csv not found."
        )

    if not BEHAVIOR_FILE.exists():

        raise FileNotFoundError(
            "attention_behavior.csv not found."
        )


    profile_df = pd.read_csv(
        PROFILE_FILE
    )

    behavior_df = pd.read_csv(
        BEHAVIOR_FILE
    )


    profile = dict(
        zip(
            profile_df["metric"],
            profile_df["value"]
        )
    )


    behavior = dict(
        zip(
            behavior_df["metric"],
            behavior_df["value"]
        )
    )


    return profile, behavior


# ============================================================
# BUILD DIGITAL TWIN CONTEXT
# ============================================================

def build_context():

    profile, behavior = load_digital_twin()


    context = f"""
MINDTRACE PERSONAL ATTENTION DIGITAL TWIN

Attention Profile:
- Focused percentage: {profile.get("focused_percentage", 0):.2f}%
- Distracted percentage: {profile.get("distracted_percentage", 0):.2f}%
- Learning percentage: {profile.get("learning_percentage", 0):.2f}%
- Break percentage: {profile.get("break_percentage", 0):.2f}%

Behavior:
- Focus duration: {behavior.get("focus_duration_seconds", 0):.0f} seconds
- Distraction events: {behavior.get("distraction_events", 0)}
- Recovery events: {behavior.get("recovery_events", 0)}
- Context switches: {behavior.get("context_switches", 0)}
- Attention baseline: {behavior.get("attention_baseline", 0):.2f}%

Average activity:
- Mouse activity: {behavior.get("average_mouse_activity", 0):.2f}
- Keyboard activity: {behavior.get("average_keyboard_activity", 0):.2f}
- Mouse clicks: {behavior.get("average_mouse_clicks", 0):.2f}
"""

    return context


# ============================================================
# GEMINI RESPONSE
# ============================================================

def ask_gemini(question):

    context = build_context()


    system_instruction = """
You are MindTrace AI, a personalized attention
analysis assistant.

You analyze behavioral data from a user's
Attention Digital Twin.

Important rules:

1. Use the provided Digital Twin data.
2. Do not invent measurements or events.
3. Clearly distinguish observations from assumptions.
4. Never claim to diagnose ADHD, anxiety, depression,
   cognitive disorders, or any medical condition.
5. Do not present attention measurements as medical
   or psychological diagnoses.
6. If the dataset is small, mention that conclusions
   are preliminary.
7. Give concise, useful and personalized answers.
8. If asked why attention changed, explain possible
   behavioral signals but do not claim certainty.
9. If the user asks for recommendations, give practical
   suggestions based on the observed behavioral pattern.
"""


    prompt = f"""
{system_instruction}

Here is the user's current Digital Twin:

{context}

User question:

{question}

Answer as MindTrace AI.
"""


    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )


    return interaction.output_text


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("🤖 MINDTRACE GEMINI AI AGENT")
    print("=" * 60)

    print("\nDigital Twin loaded successfully.")
    print("Ask a question.")
    print("Type 'exit' to stop.\n")


    while True:

        question = input("You: ")


        if question.lower().strip() == "exit":

            print("\nMindTrace stopped.")
            break


        try:

            answer = ask_gemini(
                question
            )

            print("\n🤖 MindTrace:")
            print(answer)
            print()

        except Exception as e:

            print(
                f"\n❌ Error: {e}\n"
            )