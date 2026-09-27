import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "training_data.csv"
)

PROFILE_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "attention_profile.csv"
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(DATA_FILE)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


# ==========================================
# BASIC PROFILE
# ==========================================

total_records = len(df)

focused_records = len(
    df[df["attention_label"] == "focused"]
)

distracted_records = len(
    df[df["attention_label"] == "distracted"]
)

learning_records = len(
    df[df["attention_label"] == "learning"]
)

break_records = len(
    df[df["attention_label"] == "break"]
)


# ==========================================
# PERCENTAGES
# ==========================================

if total_records > 0:

    focused_percentage = (
        focused_records / total_records
    ) * 100

    distracted_percentage = (
        distracted_records / total_records
    ) * 100

    learning_percentage = (
        learning_records / total_records
    ) * 100

    break_percentage = (
        break_records / total_records
    ) * 100

else:

    focused_percentage = 0
    distracted_percentage = 0
    learning_percentage = 0
    break_percentage = 0


# ==========================================
# ACTIVITY STATISTICS
# ==========================================

average_mouse_activity = (
    df["mouse_events"].mean()
)

average_mouse_clicks = (
    df["mouse_clicks"].mean()
)

average_keyboard_activity = (
    df["keyboard_events"].mean()
)


# ==========================================
# PROFILE DATA
# ==========================================

profile = pd.DataFrame([
    {
        "metric": "total_records",
        "value": total_records
    },
    {
        "metric": "focused_percentage",
        "value": focused_percentage
    },
    {
        "metric": "distracted_percentage",
        "value": distracted_percentage
    },
    {
        "metric": "learning_percentage",
        "value": learning_percentage
    },
    {
        "metric": "break_percentage",
        "value": break_percentage
    },
    {
        "metric": "average_mouse_activity",
        "value": average_mouse_activity
    },
    {
        "metric": "average_mouse_clicks",
        "value": average_mouse_clicks
    },
    {
        "metric": "average_keyboard_activity",
        "value": average_keyboard_activity
    }
])


# ==========================================
# SAVE PROFILE
# ==========================================

profile.to_csv(
    PROFILE_FILE,
    index=False
)


# ==========================================
# DISPLAY
# ==========================================

print("\n" + "=" * 50)

print("🧠 MINDTRACE ATTENTION DIGITAL TWIN")

print("=" * 50)

print(
    f"\nTotal records: {total_records}"
)

print(
    f"Focused: {focused_percentage:.2f}%"
)

print(
    f"Distracted: {distracted_percentage:.2f}%"
)

print(
    f"Learning: {learning_percentage:.2f}%"
)

print(
    f"Break: {break_percentage:.2f}%"
)

print(
    f"\nAverage mouse activity: "
    f"{average_mouse_activity:.2f}"
)

print(
    f"Average keyboard activity: "
    f"{average_keyboard_activity:.2f}"
)

print(
    f"\n💾 Profile saved at:"
)

print(PROFILE_FILE)