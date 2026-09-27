import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_DIR / "data" / "raw"
PROCESSED_FOLDER = PROJECT_DIR / "data" / "processed"

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================
# LOAD RAW DATA
# ==========================================

mouse_file = RAW_FOLDER / "mouse_activity.csv"
keyboard_file = RAW_FOLDER / "keyboard_activity.csv"
window_file = RAW_FOLDER / "window_activity.csv"


mouse_df = pd.read_csv(mouse_file)
keyboard_df = pd.read_csv(keyboard_file)
window_df = pd.read_csv(window_file)


print("✅ Raw data loaded")


# ==========================================
# CONVERT TIMESTAMPS
# ==========================================

mouse_df["timestamp"] = pd.to_datetime(
    mouse_df["timestamp"]
)

keyboard_df["timestamp"] = pd.to_datetime(
    keyboard_df["timestamp"]
)

window_df["timestamp"] = pd.to_datetime(
    window_df["timestamp"]
)


# ==========================================
# CREATE 1-MINUTE TIME WINDOWS
# ==========================================

mouse_df["minute"] = (
    mouse_df["timestamp"].dt.floor("1min")
)

keyboard_df["minute"] = (
    keyboard_df["timestamp"].dt.floor("1min")
)

window_df["minute"] = (
    window_df["timestamp"].dt.floor("1min")
)


# ==========================================
# MOUSE FEATURES
# ==========================================

mouse_features = (
    mouse_df
    .groupby("minute")
    .agg(
        mouse_events=("event", "count"),
        mouse_clicks=(
            "event",
            lambda x: (x == "click").sum()
        )
    )
    .reset_index()
)


# ==========================================
# KEYBOARD FEATURES
# ==========================================

keyboard_features = (
    keyboard_df
    .groupby("minute")
    .agg(
        keyboard_events=("event", "count")
    )
    .reset_index()
)


# ==========================================
# WINDOW FEATURES
# ==========================================

window_features = (
    window_df
    .groupby("minute")
    .agg(
        window_switches=("active_window", "count")
    )
    .reset_index()
)


# ==========================================
# MERGE ALL FEATURES
# ==========================================

features = pd.merge(
    mouse_features,
    keyboard_features,
    on="minute",
    how="outer"
)

features = pd.merge(
    features,
    window_features,
    on="minute",
    how="outer"
)


# ==========================================
# SORT DATA
# ==========================================

features = features.sort_values(
    by="minute"
)

features = features.reset_index(
    drop=True
)


# ==========================================
# HANDLE MISSING VALUES
# ==========================================

numeric_columns = [
    "mouse_events",
    "mouse_clicks",
    "keyboard_events",
    "window_switches"
]

features[numeric_columns] = (
    features[numeric_columns]
    .fillna(0)
)


# ==========================================
# ACTIVITY SCORE
# ==========================================

features["activity_score"] = (
    features["mouse_events"]
    + features["keyboard_events"]
    + features["window_switches"]
)


# ==========================================
# RENAME TIMESTAMP COLUMN
# ==========================================

features = features.rename(
    columns={
        "minute": "timestamp"
    }
)


# ==========================================
# SAVE DATASET
# ==========================================

output_file = (
    PROCESSED_FOLDER /
    "attention_features.csv"
)

features.to_csv(
    output_file,
    index=False
)


# ==========================================
# RESULTS
# ==========================================

print("\n" + "=" * 50)

print("🎉 FEATURE EXTRACTION COMPLETED!")

print("=" * 50)

print(f"\n📁 Saved to:")
print(output_file)

print("\n📊 Dataset shape:")
print(features.shape)

print("\n📋 Features:")
print(list(features.columns))

print("\n🔍 First 10 rows:")
print(features.head(10))