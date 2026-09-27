import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

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
# LOAD DIGITAL TWIN DATA
# ============================================================

def load_digital_twin():

    if not PROFILE_FILE.exists():
        raise FileNotFoundError(
            "attention_profile.csv not found. "
            "Run digital_twin/profile.py first."
        )

    if not BEHAVIOR_FILE.exists():
        raise FileNotFoundError(
            "attention_behavior.csv not found. "
            "Run digital_twin/behavior.py first."
        )

    profile_df = pd.read_csv(PROFILE_FILE)
    behavior_df = pd.read_csv(BEHAVIOR_FILE)

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
# GENERATE PERSONALIZED INSIGHTS
# ============================================================

def generate_insights(profile, behavior):

    insights = []

    focused = float(
        profile.get("focused_percentage", 0)
    )

    distracted = float(
        profile.get("distracted_percentage", 0)
    )

    learning = float(
        profile.get("learning_percentage", 0)
    )

    breaks = float(
        profile.get("break_percentage", 0)
    )

    distraction_events = int(
        behavior.get("distraction_events", 0)
    )

    recovery_events = int(
        behavior.get("recovery_events", 0)
    )

    context_switches = int(
        behavior.get("context_switches", 0)
    )

    focus_duration = float(
        behavior.get("focus_duration_seconds", 0)
    )

    baseline = float(
        behavior.get("attention_baseline", 0)
    )


    # --------------------------------------------------------
    # Focus pattern
    # --------------------------------------------------------

    if focused > 50:

        insights.append(
            "A relatively large portion of the collected "
            "session was labeled as focused."
        )

    else:

        insights.append(
            "The collected session contains less than half "
            "of its records labeled as focused."
        )


    # --------------------------------------------------------
    # Distraction pattern
    # --------------------------------------------------------

    if distraction_events > 0:

        insights.append(
            f"{distraction_events} distraction event(s) "
            "were detected in the collected session."
        )

    else:

        insights.append(
            "No distinct distraction transition was detected "
            "in the collected session."
        )


    # --------------------------------------------------------
    # Recovery pattern
    # --------------------------------------------------------

    if recovery_events > 0:

        insights.append(
            f"The session contains {recovery_events} "
            "focused recovery transition(s) after distraction."
        )

    else:

        insights.append(
            "No focused recovery transition was detected "
            "after a distraction event."
        )


    # --------------------------------------------------------
    # Context switching
    # --------------------------------------------------------

    if context_switches > 3:

        insights.append(
            f"There were {context_switches} context switches, "
            "which indicates frequent changes in active windows "
            "during this collected session."
        )

    else:

        insights.append(
            f"The session recorded {context_switches} "
            "context switch(es)."
        )


    # --------------------------------------------------------
    # Focus duration
    # --------------------------------------------------------

    insights.append(
        f"The accumulated focused duration in the collected "
        f"session was approximately {focus_duration:.0f} seconds."
    )


    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    insights.append(
        f"The current personalized focus baseline is "
        f"{baseline:.2f}% based on the available labeled data."
    )


    return insights


# ============================================================
# ANSWER USER QUESTION
# ============================================================

def ask_mindtrace(question):

    profile, behavior = load_digital_twin()

    question = question.lower().strip()

    focused = float(
        profile.get("focused_percentage", 0)
    )

    distracted = float(
        profile.get("distracted_percentage", 0)
    )

    learning = float(
        profile.get("learning_percentage", 0)
    )

    breaks = float(
        profile.get("break_percentage", 0)
    )

    distraction_events = int(
        behavior.get("distraction_events", 0)
    )

    recovery_events = int(
        behavior.get("recovery_events", 0)
    )

    context_switches = int(
        behavior.get("context_switches", 0)
    )

    focus_duration = float(
        behavior.get("focus_duration_seconds", 0)
    )

    baseline = float(
        behavior.get("attention_baseline", 0)
    )


    # ========================================================
    # QUESTION: WHY DID ATTENTION DROP?
    # ========================================================

    if (
        "why" in question
        and (
            "attention" in question
            or "focus" in question
        )
        and (
            "drop" in question
            or "low" in question
            or "distract" in question
        )
    ):

        response = (
            "🧠 MindTrace Analysis\n\n"
            f"Your current focused baseline is "
            f"{baseline:.2f}% based on the collected data.\n\n"
        )

        if distraction_events > 0:

            response += (
                f"I detected {distraction_events} "
                "distinct distraction event(s). "
            )

        else:

            response += (
                "I did not detect a distinct distraction "
                "transition in this session. "
            )

        if context_switches > 0:

            response += (
                f"The session also contained "
                f"{context_switches} context switch(es), "
                "which may indicate changes in active tasks "
                "or applications. "
            )

        response += (
            "\n\nThis is a behavioral observation from the "
            "collected session, not a medical or psychological "
            "diagnosis."
        )

        return response


    # ========================================================
    # QUESTION: HOW IS MY ATTENTION?
    # ========================================================

    if (
        "how" in question
        and (
            "attention" in question
            or "focus" in question
        )
    ):

        return (
            "🧠 Your MindTrace Attention Profile\n\n"
            f"🟢 Focused: {focused:.1f}%\n"
            f"🔴 Distracted: {distracted:.1f}%\n"
            f"🔵 Learning: {learning:.1f}%\n"
            f"🟡 Break: {breaks:.1f}%\n\n"
            f"⏱️ Focus duration: "
            f"{focus_duration:.0f} seconds\n"
            f"🔄 Recovery events: {recovery_events}\n"
            f"🖥️ Context switches: {context_switches}\n"
        )


    # ========================================================
    # QUESTION: DISTRACTION
    # ========================================================

    if (
        "distraction" in question
        or "distracted" in question
    ):

        return (
            "🔴 Distraction Analysis\n\n"
            f"Detected distraction events: "
            f"{distraction_events}\n\n"
            f"Context switches: {context_switches}\n\n"
            "MindTrace uses these behavioral signals to "
            "describe patterns in your collected session. "
            "It does not determine the cause of distraction "
            "with certainty."
        )


    # ========================================================
    # QUESTION: FOCUS
    # ========================================================

    if (
        "focus" in question
        or "focused" in question
    ):

        return (
            "🎯 Focus Analysis\n\n"
            f"Focused activity: {focused:.1f}%\n"
            f"Focus duration: {focus_duration:.0f} seconds\n"
            f"Attention baseline: {baseline:.2f}%\n\n"
            "For a more stable personal baseline, MindTrace "
            "should collect multiple sessions across different "
            "tasks and days."
        )


    # ========================================================
    # QUESTION: SUMMARY
    # ========================================================

    if (
        "summary" in question
        or "report" in question
        or "profile" in question
    ):

        insights = generate_insights(
            profile,
            behavior
        )

        response = (
            "🧠 MindTrace Personal Attention Report\n\n"
        )

        for insight in insights:

            response += (
                "• " + insight + "\n"
            )

        return response


    # ========================================================
    # DEFAULT RESPONSE
    # ========================================================

    return (
        "🤖 I can analyze your MindTrace attention data.\n\n"
        "Try asking:\n"
        "• Why did my attention drop?\n"
        "• How is my attention?\n"
        "• Show my focus profile\n"
        "• What is my distraction pattern?\n"
        "• Give me a summary report"
    )


# ============================================================
# TEST AGENT
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("🤖 MINDTRACE AI AGENT")
    print("=" * 60)

    print("\nAsk a question about your attention.")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower().strip() == "exit":

            print("\nMindTrace Agent stopped.")
            break

        try:

            answer = ask_mindtrace(
                question
            )

            print("\nMindTrace:")
            print(answer)

        except Exception as e:

            print(
                f"\n❌ Error: {e}"
            )