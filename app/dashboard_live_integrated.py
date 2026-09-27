import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import json

from ai_agent.gemini_agent import ask_gemini


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MindTrace AI",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# FILE PATHS
# ============================================================

TRAINING_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "training_data.csv"
)

MODEL_FILE = (
    PROJECT_DIR
    / "models"
    / "attention_model.pkl"
)

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
# TITLE
# ============================================================

st.title("🧠 MindTrace AI")

st.subheader(
    "Personal Attention & Cognitive Drift Analyzer"
)

st.write(
    "MindTrace learns behavioral patterns from mouse, "
    "keyboard and window activity to analyze attention states."
)


# ============================================================
# LOAD TRAINING DATA
# ============================================================

if not TRAINING_FILE.exists():

    st.error(
        "Training data not found. "
        "Please run the training session first."
    )

    st.stop()


df = pd.read_csv(TRAINING_FILE)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

df = df.dropna(
    subset=["timestamp"]
)

df = df.sort_values(
    "timestamp"
).reset_index(drop=True)


# ============================================================
# LOAD MACHINE LEARNING MODEL
# ============================================================

model = None

if MODEL_FILE.exists():

    try:

        model = joblib.load(
            MODEL_FILE
        )

    except Exception as e:

        st.warning(
            f"Model could not be loaded: {e}"
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ MindTrace Controls")

st.sidebar.write(
    "### Project Status"
)

st.sidebar.success(
    "🟢 Data Collection Ready"
)


if model is not None:

    st.sidebar.success(
        "🟢 ML Model Loaded"
    )

else:

    st.sidebar.warning(
        "🟡 ML Model Not Available"
    )


if PROFILE_FILE.exists() and BEHAVIOR_FILE.exists():

    st.sidebar.success(
        "🟢 Digital Twin Ready"
    )

else:

    st.sidebar.warning(
        "🟡 Digital Twin Not Ready"
    )


st.sidebar.markdown("---")

st.sidebar.write(
    "### 🔐 Privacy"
)

st.sidebar.info(
    "MindTrace stores behavioral activity counts "
    "rather than actual keyboard keys."
)


# ============================================================
# CURRENT ATTENTION STATE
# ============================================================

st.header("🎯 Current Attention State")

latest_row = df.iloc[-1]

current_prediction = "Unknown"
current_confidence = 0.0


if model is not None:

    try:

        features =pd.DataFrame( [[
            latest_row["mouse_events"],
            latest_row["mouse_clicks"],
            latest_row["keyboard_events"]
        ]],
        columns=[
        "mouse_events",
        "mouse_clicks",
        "keyboard_events"
        ]
            )


        current_prediction = model.predict(
            features
        )[0]


        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                features
            )[0]

            current_confidence = (
                max(probabilities) * 100
            )

    except Exception:

        current_prediction = (
            latest_row.get(
                "attention_label",
                "Unknown"
            )
        )


# ============================================================
# CURRENT STATE METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🧠 Attention State",
        str(current_prediction).upper()
    )


with col2:

    st.metric(
        "🎯 Confidence",
        f"{current_confidence:.2f}%"
    )


with col3:

    st.metric(
        "🖱️ Mouse Events",
        int(latest_row["mouse_events"])
    )


with col4:

    st.metric(
        "⌨️ Keyboard Events",
        int(latest_row["keyboard_events"])
    )


# ============================================================
# 🔴 LIVE ATTENTION ENGINE
# ============================================================

LIVE_STATE_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "live_state.json"
)

st.markdown("---")
st.header("🔴 Live Attention Engine")
st.caption(
    "Reads the latest state produced by live_mindtrace.py. "
    "This section is independent from the historical dashboard data."
)

if LIVE_STATE_FILE.exists():

    try:
        with open(LIVE_STATE_FILE, "r", encoding="utf-8") as f:
            live_state = json.load(f)

        if live_state.get("running") is False:
            st.warning("⏸️ Live Attention Engine is currently stopped.")
        else:
            st.success("🟢 Live Attention Engine is running")

        live_prediction = str(live_state.get("prediction", "Unknown"))
        live_confidence = float(live_state.get("confidence", 0))
        live_app = str(live_state.get("active_app", "Unknown"))
        live_mouse = int(live_state.get("mouse_events", 0))
        live_clicks = int(live_state.get("mouse_clicks", 0))
        live_keyboard = int(live_state.get("keyboard_events", 0))

        live_col1, live_col2, live_col3, live_col4 = st.columns(4)

        with live_col1:
            st.metric("🧠 Live State", live_prediction.upper())

        with live_col2:
            st.metric("🎯 Live Confidence", f"{live_confidence:.2f}%")

        with live_col3:
            st.metric("🖥️ Active App", live_app)

        with live_col4:
            st.metric("🖱️ Mouse Events", live_mouse)

        live_col5, live_col6, live_col7 = st.columns(3)

        with live_col5:
            st.metric("🖱️ Mouse Clicks", live_clicks)

        with live_col6:
            st.metric("⌨️ Keyboard Events", live_keyboard)

        with live_col7:
            st.metric("🕒 Last Update", str(live_state.get("timestamp", "Unknown")))

        st.caption(
            "Note: the current ML model predicts from mouse events, mouse clicks, "
            "and keyboard-event counts. Active app is displayed as context only."
        )

        if st.button("🔄 Refresh Live State", key="refresh_live_state"):
            st.rerun()

    except Exception as e:
        st.error(f"Could not read live_state.json: {e}")

else:
    st.info(
        "🔵 Live state not available yet. Start "
        "data_collection/live_mindtrace.py and this section will appear."
    )


# ============================================================
# STATE MESSAGE
# ============================================================

if str(current_prediction).lower() == "focused":

    st.success(
        "🟢 You appear to be in a focused state."
    )

elif str(current_prediction).lower() == "distracted":

    st.warning(
        "🔴 Attention drift detected."
    )

elif str(current_prediction).lower() == "learning":

    st.info(
        "🔵 Learning activity detected."
    )

elif str(current_prediction).lower() == "break":

    st.info(
        "🟡 Break state detected."
    )


# ============================================================
# ACTIVITY SUMMARY
# ============================================================

st.markdown("---")

st.header("📊 Activity Summary")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Mouse Activity",
        f"{df['mouse_events'].mean():.2f}"
    )


with col2:

    st.metric(
        "Average Keyboard Activity",
        f"{df['keyboard_events'].mean():.2f}"
    )


with col3:

    st.metric(
        "Average Mouse Clicks",
        f"{df['mouse_clicks'].mean():.2f}"
    )


# ============================================================
# 🧠 ATTENTION DIGITAL TWIN
# ============================================================

st.markdown("---")

st.header("🧠 My Attention Digital Twin")

st.write(
    "Your personalized attention profile based on "
    "your collected behavioral activity."
)


if PROFILE_FILE.exists() and BEHAVIOR_FILE.exists():

    profile_df = pd.read_csv(
        PROFILE_FILE
    )

    behavior_df = pd.read_csv(
        BEHAVIOR_FILE
    )


    # --------------------------------------------------------
    # Convert Profile to Dictionary
    # --------------------------------------------------------

    profile_data = dict(
        zip(
            profile_df["metric"],
            profile_df["value"]
        )
    )


    # --------------------------------------------------------
    # Convert Behavior to Dictionary
    # --------------------------------------------------------

    behavior_data = dict(
        zip(
            behavior_df["metric"],
            behavior_df["value"]
        )
    )


    # ========================================================
    # ATTENTION PATTERN
    # ========================================================

    st.subheader(
        "🎯 Attention Pattern"
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🟢 Focused",
            f"{profile_data.get('focused_percentage', 0):.1f}%"
        )


    with col2:

        st.metric(
            "🔴 Distracted",
            f"{profile_data.get('distracted_percentage', 0):.1f}%"
        )


    with col3:

        st.metric(
            "🔵 Learning",
            f"{profile_data.get('learning_percentage', 0):.1f}%"
        )


    with col4:

        st.metric(
            "🟡 Break",
            f"{profile_data.get('break_percentage', 0):.1f}%"
        )


    # ========================================================
    # BEHAVIORAL CHARACTERISTICS
    # ========================================================

    st.subheader(
        "📊 Behavioral Characteristics"
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "⏱️ Focus Duration",
            f"{behavior_data.get('focus_duration_seconds', 0):.0f} sec"
        )


    with col2:

        st.metric(
            "🔴 Distraction Events",
            f"{behavior_data.get('distraction_events', 0):.0f}"
        )


    with col3:

        st.metric(
            "🔄 Recovery Events",
            f"{behavior_data.get('recovery_events', 0):.0f}"
        )


    with col4:

        st.metric(
            "🖥️ Context Switches",
            f"{behavior_data.get('context_switches', 0):.0f}"
        )


    # ========================================================
    # PERSONAL ATTENTION BASELINE
    # ========================================================

    st.subheader(
        "📈 Personal Attention Baseline"
    )

    baseline = float(
        behavior_data.get(
            "attention_baseline",
            0
        )
    )


    st.progress(
        min(
            max(baseline / 100, 0),
            1
        )
    )


    st.write(
        f"Your current collected attention baseline is "
        f"**{baseline:.2f}% focused activity.**"
    )


    # ========================================================
    # TYPICAL ACTIVITY
    # ========================================================

    st.subheader(
        "⚙️ Typical Activity"
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🖱️ Mouse Activity",
            f"{behavior_data.get('average_mouse_activity', 0):.2f}"
        )


    with col2:

        st.metric(
            "⌨️ Keyboard Activity",
            f"{behavior_data.get('average_keyboard_activity', 0):.2f}"
        )


    with col3:

        st.metric(
            "🖱️ Mouse Clicks",
            f"{behavior_data.get('average_mouse_clicks', 0):.2f}"
        )


else:

    st.warning(
        "Digital Twin data not found. "
        "Run profile.py and behavior.py first."
    )


# ============================================================
# ATTENTION DISTRIBUTION
# ============================================================

st.markdown("---")

st.header("🥧 Attention Distribution")


if "attention_label" in df.columns:

    label_counts = (
        df["attention_label"]
        .value_counts()
        .reset_index()
    )

    label_counts.columns = [
        "attention_label",
        "count"
    ]


    label_counts = label_counts[
        label_counts["attention_label"] != "unknown"
    ]


    if len(label_counts) > 0:

        fig_pie = px.pie(
            label_counts,
            names="attention_label",
            values="count",
            title="Attention State Distribution"
        )


        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    else:

        st.info(
            "No labeled attention data available yet."
        )


# ============================================================
# ACTIVITY OVER TIME
# ============================================================

st.markdown("---")

st.header("📈 Activity Over Time")


activity_df = df.copy()


activity_df["total_activity"] = (
    activity_df["mouse_events"]
    + activity_df["keyboard_events"]
    + activity_df["mouse_clicks"]
)


fig_activity = px.line(
    activity_df,
    x="timestamp",
    y="total_activity",
    title="Behavioral Activity Over Time",
    labels={
        "timestamp": "Time",
        "total_activity": "Activity"
    }
)


st.plotly_chart(
    fig_activity,
    use_container_width=True
)


# ============================================================
# ATTENTION TIMELINE
# ============================================================

st.header("🧠 Attention Timeline")


if "attention_label" in df.columns:

    timeline_df = df[
        df["attention_label"] != "unknown"
    ].copy()


    if len(timeline_df) > 0:

        fig_timeline = px.scatter(
            timeline_df,
            x="timestamp",
            y="attention_label",
            title="Attention State Timeline",
            labels={
                "timestamp": "Time",
                "attention_label": "Attention State"
            }
        )


        st.plotly_chart(
            fig_timeline,
            use_container_width=True
        )

    else:

        st.info(
            "No attention labels available."
        )


# ============================================================
# MACHINE LEARNING MODEL
# ============================================================

st.markdown("---")

st.header("🤖 Machine Learning Model")


if model is not None:

    st.success(
        "Random Forest Attention Classifier loaded."
    )

    st.write(
        "The model currently uses:"
    )

    st.code(
        """
Mouse Events
Mouse Clicks
Keyboard Events
        """
    )

else:

    st.warning(
        "Attention model not loaded."
    )


# ============================================================
# RECENT BEHAVIORAL DATA
# ============================================================

st.markdown("---")

st.header("📋 Recent Behavioral Data")


st.dataframe(
    df.tail(20),
    use_container_width=True
)


# ============================================================
# PRIVACY NOTE
# ============================================================

st.markdown("---")

st.info(
    "🔐 Privacy: MindTrace records behavioral activity "
    "patterns rather than actual keyboard characters. "
    "The goal is to analyze attention patterns while "
    "minimizing sensitive data collection."
)


# ============================================================
# 🤖 MINDTRACE GEMINI AI AGENT
# ============================================================

st.markdown("---")

st.header("🤖 Ask MindTrace AI")

st.write(
    "Talk to your personalized Attention Digital Twin "
    "using natural language."
)


# ============================================================
# CHAT SESSION
# ============================================================

if "mindtrace_chat" not in st.session_state:

    st.session_state.mindtrace_chat = []


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.markdown("### 💡 Try asking")


example_questions = [
    "How is my attention?",
    "Why did my attention drop?",
    "What is my distraction pattern?",
    "Show my focus profile",
    "What can I improve?"
]


cols = st.columns(5)


for i, question in enumerate(example_questions):

    with cols[i]:

        if st.button(
            question,
            key=f"gemini_question_{i}"
        ):

            st.session_state[
                "pending_question"
            ] = question


# ============================================================
# DISPLAY PREVIOUS CHAT
# ============================================================

for message in st.session_state.mindtrace_chat:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Ask anything about your attention..."
)


# ============================================================
# HANDLE EXAMPLE QUESTION
# ============================================================

if "pending_question" in st.session_state:

    user_question = st.session_state.pop(
        "pending_question"
    )


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if user_question:

    # --------------------------------------------------------
    # Store user message
    # --------------------------------------------------------

    st.session_state.mindtrace_chat.append(
        {
            "role": "user",
            "content": user_question
        }
    )


    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            user_question
        )


    # --------------------------------------------------------
    # Gemini response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 MindTrace is analyzing your Digital Twin..."
        ):

            try:

                response = ask_gemini(
                    user_question
                )


                st.markdown(
                    response
                )


                # Save assistant response
                st.session_state.mindtrace_chat.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )


            except Exception as e:

                error_message = (
                    f"❌ Gemini Agent Error:\n\n{e}"
                )


                st.error(
                    error_message
                )


# ============================================================
# CHAT CONTROLS
# ============================================================

st.markdown("---")

col1, col2 = st.columns(
    [1, 4]
)


with col1:

    if st.button(
        "🗑️ Clear Chat"
    ):

        st.session_state.mindtrace_chat = []

        st.rerun()


with col2:

    st.caption(
        "🔐 Gemini receives derived Digital Twin metrics, "
        "not raw keyboard characters."
    )


# ============================================================
# AGENT INFORMATION
# ============================================================

with st.expander(
    "ℹ️ How does MindTrace AI work?"
):

    st.write(
        """
        MindTrace AI combines:

        🧠 Attention Digital Twin
        ├── Focus percentage
        ├── Distraction percentage
        ├── Learning percentage
        ├── Break percentage
        ├── Focus duration
        ├── Distraction events
        ├── Recovery events
        └── Context switches

                    ↓

              🤖 Gemini AI

                    ↓

        Personalized attention analysis

        The AI uses behavioral data as context.

        It does not diagnose medical or psychological
        conditions.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "MindTrace AI • Personal Attention & Cognitive Drift Analyzer"
)