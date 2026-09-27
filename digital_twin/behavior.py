import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "training_data.csv"
)

BEHAVIOR_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "attention_behavior.csv"
)

df = pd.read_csv(DATA_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)


# --------------------------------------------------
# 1. Focus Duration
# --------------------------------------------------

focused_df = df[df["attention_label"] == "focused"]

if len(focused_df) > 0:
    focus_duration_seconds = len(focused_df)
else:
    focus_duration_seconds = 0


# --------------------------------------------------
# 2. Distraction Events
# --------------------------------------------------

labels = df["attention_label"].tolist()

distraction_events = 0

for i in range(1, len(labels)):
    if (
        labels[i] == "distracted"
        and labels[i - 1] != "distracted"
    ):
        distraction_events += 1


# --------------------------------------------------
# 3. Recovery Events
# --------------------------------------------------

recovery_events = 0

for i in range(1, len(labels)):
    if (
        labels[i - 1] == "distracted"
        and labels[i] == "focused"
    ):
        recovery_events += 1


# --------------------------------------------------
# 4. Context Switching
# --------------------------------------------------

context_switches = 0

if "active_window" in df.columns:

    previous_window = None

    for window in df["active_window"]:

        if previous_window is not None:

            if window != previous_window:
                context_switches += 1

        previous_window = window


# --------------------------------------------------
# 5. Attention Baseline
# --------------------------------------------------

attention_counts = df["attention_label"].value_counts()

if len(df) > 0:

    attention_baseline = (
        attention_counts.get("focused", 0) / len(df)
    ) * 100

else:

    attention_baseline = 0


# --------------------------------------------------
# 6. Average Activity
# --------------------------------------------------

average_mouse = df["mouse_events"].mean()
average_keyboard = df["keyboard_events"].mean()
average_clicks = df["mouse_clicks"].mean()


# --------------------------------------------------
# Save Behavior Profile
# --------------------------------------------------

behavior = pd.DataFrame([
    {
        "metric": "focus_duration_seconds",
        "value": focus_duration_seconds
    },
    {
        "metric": "distraction_events",
        "value": distraction_events
    },
    {
        "metric": "recovery_events",
        "value": recovery_events
    },
    {
        "metric": "context_switches",
        "value": context_switches
    },
    {
        "metric": "attention_baseline",
        "value": attention_baseline
    },
    {
        "metric": "average_mouse_activity",
        "value": average_mouse
    },
    {
        "metric": "average_keyboard_activity",
        "value": average_keyboard
    },
    {
        "metric": "average_mouse_clicks",
        "value": average_clicks
    }
])

behavior.to_csv(BEHAVIOR_FILE, index=False)


# --------------------------------------------------
# Display
# --------------------------------------------------

print("\n" + "=" * 55)
print("🧠 MINDTRACE — ATTENTION BEHAVIOR ANALYSIS")
print("=" * 55)

print(f"\n⏱️ Focus duration: {focus_duration_seconds} seconds")
print(f"🔴 Distraction events: {distraction_events}")
print(f"🔄 Recovery events: {recovery_events}")
print(f"🖥️ Context switches: {context_switches}")
print(f"📊 Attention baseline: {attention_baseline:.2f}%")

print("\n📈 Activity:")
print(f"Mouse activity: {average_mouse:.2f}")
print(f"Keyboard activity: {average_keyboard:.2f}")
print(f"Mouse clicks: {average_clicks:.2f}")

print("\n💾 Behavior profile saved at:")
print(BEHAVIOR_FILE)