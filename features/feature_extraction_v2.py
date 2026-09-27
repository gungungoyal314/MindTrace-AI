import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "attention_features_v2.csv"


# ============================================================
# INPUT FILES
# ============================================================

MOUSE_FILE = RAW_DIR / "mouse_activity.csv"
KEYBOARD_FILE = RAW_DIR / "keyboard_activity.csv"
WINDOW_FILE = RAW_DIR / "window_activity.csv"


# ============================================================
# HEADER
# ============================================================

print("=" * 65)
print("MINDTRACE AI - FEATURE EXTRACTION V2")
print("=" * 65)


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

required_files = [
    MOUSE_FILE,
    KEYBOARD_FILE,
    WINDOW_FILE
]

for file in required_files:

    if not file.exists():

        raise FileNotFoundError(
            f"\nRequired file not found:\n{file}"
        )


# ============================================================
# LOAD RAW DATA
# ============================================================

print("\nLoading raw activity data...")

mouse = pd.read_csv(MOUSE_FILE)
keyboard = pd.read_csv(KEYBOARD_FILE)
window = pd.read_csv(WINDOW_FILE)

print("Mouse data loaded")
print("Keyboard data loaded")
print("Window data loaded")


# ============================================================
# DISPLAY COLUMNS
# ============================================================

print("\nChecking columns...")

print("Mouse columns:", list(mouse.columns))
print("Keyboard columns:", list(keyboard.columns))
print("Window columns:", list(window.columns))


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

if "timestamp" not in mouse.columns:
    raise KeyError("timestamp column missing in mouse_activity.csv")

if "event" not in mouse.columns:
    raise KeyError("event column missing in mouse_activity.csv")

if "timestamp" not in keyboard.columns:
    raise KeyError("timestamp column missing in keyboard_activity.csv")

if "event" not in keyboard.columns:
    raise KeyError("event column missing in keyboard_activity.csv")

if "timestamp" not in window.columns:
    raise KeyError("timestamp column missing in window_activity.csv")

if "active_window" not in window.columns:
    raise KeyError(
        "active_window column missing in window_activity.csv"
    )


# ============================================================
# CONVERT TIMESTAMPS
# ============================================================

mouse["timestamp"] = pd.to_datetime(
    mouse["timestamp"],
    errors="coerce"
)

keyboard["timestamp"] = pd.to_datetime(
    keyboard["timestamp"],
    errors="coerce"
)

window["timestamp"] = pd.to_datetime(
    window["timestamp"],
    errors="coerce"
)


# ============================================================
# REMOVE INVALID TIMESTAMPS
# ============================================================

mouse = mouse.dropna(
    subset=["timestamp"]
).copy()

keyboard = keyboard.dropna(
    subset=["timestamp"]
).copy()

window = window.dropna(
    subset=["timestamp"]
).copy()


# ============================================================
# CREATE MINUTE WINDOWS
# ============================================================

mouse["minute"] = (
    mouse["timestamp"].dt.floor("min")
)

keyboard["minute"] = (
    keyboard["timestamp"].dt.floor("min")
)

window["minute"] = (
    window["timestamp"].dt.floor("min")
)


# ============================================================
# MOUSE FEATURES
# ============================================================

print("\nExtracting mouse features...")

mouse_features = (
    mouse
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


# ============================================================
# KEYBOARD FEATURES
# ============================================================

print("Extracting keyboard features...")

keyboard_features = (
    keyboard
    .groupby("minute")
    .agg(
        keyboard_events=("event", "count")
    )
    .reset_index()
)


# ============================================================
# WINDOW / CONTEXT SWITCH FEATURES
# ============================================================

print("Extracting context-switch features...")

# Sort chronologically
window = (
    window
    .sort_values("timestamp")
    .reset_index(drop=True)
)


# Detect active-window changes
window["window_changed"] = (
    window["active_window"]
    .ne(window["active_window"].shift())
    .astype(int)
)


# First observed window is not a switch
if len(window) > 0:

    window.loc[
        window.index[0],
        "window_changed"
    ] = 0


# Count switches per minute
window_features = (
    window
    .groupby("minute")
    .agg(
        context_switches=(
            "window_changed",
            "sum"
        )
    )
    .reset_index()
)


# ============================================================
# ACTIVE SECONDS
# ============================================================

print("Calculating active seconds...")


# Combine mouse and keyboard timestamps
activity_times = pd.concat(
    [
        mouse[["timestamp"]],
        keyboard[["timestamp"]]
    ],
    ignore_index=True
)


if len(activity_times) > 0:

    # Round timestamps to seconds
    activity_times["second"] = (
        activity_times["timestamp"]
        .dt.floor("s")
    )

    # One active second should count only once
    activity_times = (
        activity_times[
            ["second"]
        ]
        .drop_duplicates()
    )

    # Create minute column
    activity_times["minute"] = (
        activity_times["second"]
        .dt.floor("min")
    )

    # Count active seconds
    active_seconds = (
        activity_times
        .groupby("minute")
        .size()
        .reset_index(
            name="active_seconds"
        )
    )

else:

    active_seconds = pd.DataFrame(
        columns=[
            "minute",
            "active_seconds"
        ]
    )


# ============================================================
# MERGE ALL FEATURES
# ============================================================

print("\nCombining features...")

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

features = pd.merge(
    features,
    active_seconds,
    on="minute",
    how="outer"
)


# ============================================================
# SORT
# ============================================================

features = (
    features
    .sort_values("minute")
    .reset_index(drop=True)
)


# ============================================================
# FILL MISSING VALUES
# ============================================================

numeric_columns = [
    "mouse_events",
    "mouse_clicks",
    "keyboard_events",
    "context_switches",
    "active_seconds"
]

for column in numeric_columns:

    if column not in features.columns:
        features[column] = 0

    features[column] = (
        features[column]
        .fillna(0)
    )


# ============================================================
# INTEGER CONVERSION
# ============================================================

integer_columns = [
    "mouse_events",
    "mouse_clicks",
    "keyboard_events",
    "context_switches",
    "active_seconds"
]

for column in integer_columns:

    features[column] = (
        features[column]
        .astype(int)
    )


# ============================================================
# ACTIVITY SCORE
# ============================================================

print("Calculating activity score...")

features["activity_score"] = (
    features["mouse_events"]
    + features["mouse_clicks"]
    + features["keyboard_events"]
)


# ============================================================
# ACTIVITY RATE
# ============================================================

print("Calculating activity rate...")

features["activity_rate"] = (
    features["active_seconds"] / 60
)

features["activity_rate"] = (
    features["activity_rate"]
    .clip(
        lower=0,
        upper=1
    )
)


# ============================================================
# IDLE TIME
# ============================================================

print("Calculating idle time...")

features["idle_time_seconds"] = (
    60 - features["active_seconds"]
)

features["idle_time_seconds"] = (
    features["idle_time_seconds"]
    .clip(
        lower=0,
        upper=60
    )
)

features["idle_time_seconds"] = (
    features["idle_time_seconds"]
    .astype(int)
)


# ============================================================
# ACTIVITY TREND
# ============================================================

print("Calculating activity trend...")

features["activity_trend"] = (
    features["activity_score"]
    .diff()
    .fillna(0)
)


# ============================================================
# ROUND VALUES
# ============================================================

features["activity_rate"] = (
    features["activity_rate"]
    .round(3)
)

features["activity_trend"] = (
    features["activity_trend"]
    .round(2)
)


# ============================================================
# FINAL COLUMN ORDER
# ============================================================

final_columns = [
    "minute",
    "mouse_events",
    "mouse_clicks",
    "keyboard_events",
    "context_switches",
    "active_seconds",
    "activity_score",
    "activity_rate",
    "idle_time_seconds",
    "activity_trend"
]

features = features[
    final_columns
]


# ============================================================
# SAVE DATASET
# ============================================================

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

features.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# DISPLAY DATASET
# ============================================================

print("\n" + "=" * 65)
print("GENERATED FEATURE DATASET")
print("=" * 65)

print(
    features.to_string(
        index=False
    )
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 65)
print("VALIDATION")
print("=" * 65)


# Check idle time
idle_valid = (
    features["idle_time_seconds"]
    .between(0, 60)
    .all()
)

if idle_valid:

    print(
        "OK - Idle time values are valid (0-60 seconds)"
    )

else:

    print(
        "ERROR - Invalid idle time detected!"
    )


# Check activity rate
rate_valid = (
    features["activity_rate"]
    .between(0, 1)
    .all()
)

if rate_valid:

    print(
        "OK - Activity rate values are valid (0-1)"
    )

else:

    print(
        "ERROR - Invalid activity rate detected!"
    )


# Check negative counts
count_columns = [
    "mouse_events",
    "mouse_clicks",
    "keyboard_events",
    "context_switches",
    "active_seconds",
    "activity_score"
]

counts_valid = (
    features[count_columns]
    .ge(0)
    .all()
    .all()
)

if counts_valid:

    print(
        "OK - No negative activity counts"
    )

else:

    print(
        "ERROR - Negative activity count detected!"
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 65)
print("FEATURE DATASET CREATED SUCCESSFULLY!")
print("=" * 65)

print(
    f"\nSaved at:\n{OUTPUT_FILE}"
)

print(
    f"\nTotal rows: {len(features)}"
)

print(
    f"Total columns: {len(features.columns)}"
)

print(
    "\nMindTrace Feature Extraction V2 completed."
)