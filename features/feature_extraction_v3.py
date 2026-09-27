import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

INPUT_FILE = PROCESSED_DIR / "attention_features_v2.csv"
WINDOW_FILE = RAW_DIR / "window_activity.csv"

OUTPUT_FILE = PROCESSED_DIR / "attention_features_v3.csv"


# ============================================================
# HEADER
# ============================================================

print("=" * 65)
print("MINDTRACE AI - FEATURE EXTRACTION V3")
print("=" * 65)


# ============================================================
# CHECK FILES
# ============================================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"V2 feature file not found:\n{INPUT_FILE}"
    )

if not WINDOW_FILE.exists():
    raise FileNotFoundError(
        f"Window activity file not found:\n{WINDOW_FILE}"
    )


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading V2 features...")

features = pd.read_csv(INPUT_FILE)

print("Loading window activity...")

window = pd.read_csv(WINDOW_FILE)


# ============================================================
# CHECK WINDOW COLUMNS
# ============================================================

if "timestamp" not in window.columns:
    raise KeyError(
        "timestamp column missing in window_activity.csv"
    )

if "active_window" not in window.columns:
    raise KeyError(
        "active_window column missing in window_activity.csv"
    )


# ============================================================
# CONVERT TIMESTAMP
# ============================================================

window["timestamp"] = pd.to_datetime(
    window["timestamp"],
    errors="coerce"
)

window = window.dropna(
    subset=["timestamp"]
).copy()


# ============================================================
# APP CATEGORY FUNCTION
# ============================================================

def categorize_window(title):

    if pd.isna(title):
        return "Other"

    title = str(title).lower()

    # IDE / Coding
    if any(word in title for word in [
        "visual studio code",
        "vs code",
        "pycharm",
        "jupyter",
        "python",
        "programiz",
        "terminal",
        "command prompt",
        "powershell"
    ]):
        return "IDE"

    # Browser
    if any(word in title for word in [
        "google chrome",
        "microsoft edge",
        "firefox",
        "brave",
        "opera"
    ]):
        return "Browser"

    # Messaging
    if any(word in title for word in [
        "whatsapp",
        "telegram",
        "messenger",
        "discord"
    ]):
        return "Messaging"

    # Social Media
    if any(word in title for word in [
        "instagram",
        "facebook",
        "twitter",
        "x.com",
        "linkedin"
    ]):
        return "Social Media"

    # Entertainment
    if any(word in title for word in [
        "youtube",
        "netflix",
        "spotify",
        "prime video"
    ]):
        return "Entertainment"

    # Documents
    if any(word in title for word in [
        "microsoft word",
        "word",
        ".doc",
        ".docx",
        "notepad"
    ]):
        return "Document"

    # Spreadsheet
    if any(word in title for word in [
        "microsoft excel",
        "excel",
        ".xlsx",
        ".csv"
    ]):
        return "Spreadsheet"

    # Presentation
    if any(word in title for word in [
        "powerpoint",
        "power point",
        ".ppt",
        ".pptx"
    ]):
        return "Presentation"

    # Learning
    if any(word in title for word in [
        "coursera",
        "udemy",
        "khan academy",
        "geeksforgeeks",
        "w3schools"
    ]):
        return "Learning"

    return "Other"


# ============================================================
# CATEGORIZE WINDOWS
# ============================================================

print("\nCategorizing active windows...")

window["app_category"] = (
    window["active_window"]
    .apply(categorize_window)
)


# ============================================================
# CREATE MINUTE
# ============================================================

window["minute"] = (
    window["timestamp"]
    .dt.floor("min")
)


# ============================================================
# FIND DOMINANT APP CATEGORY
# ============================================================

print("Finding dominant app category per minute...")


def dominant_category(series):

    counts = series.value_counts()

    if len(counts) == 0:
        return "Other"

    return counts.index[0]


app_features = (
    window
    .groupby("minute")
    .agg(
        active_app_category=(
            "app_category",
            dominant_category
        )
    )
    .reset_index()
)


# ============================================================
# MERGE WITH V2 FEATURES
# ============================================================

print("Combining V2 features with app category...")

features["minute"] = pd.to_datetime(
    features["minute"],
    errors="coerce"
)

features = features.dropna(
    subset=["minute"]
).copy()


features = pd.merge(
    features,
    app_features,
    on="minute",
    how="left"
)


# ============================================================
# HANDLE MISSING CATEGORY
# ============================================================

features["active_app_category"] = (
    features["active_app_category"]
    .fillna("Other")
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
    "activity_trend",
    "active_app_category"
]


features = features[
    final_columns
]


# ============================================================
# SAVE
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
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 65)
print("GENERATED FEATURE DATASET V3")
print("=" * 65)

print(
    features.to_string(
        index=False
    )
)


# ============================================================
# SHOW APP CATEGORY DISTRIBUTION
# ============================================================

print("\n" + "=" * 65)
print("APP CATEGORY DISTRIBUTION")
print("=" * 65)

print(
    features["active_app_category"]
    .value_counts()
)


# ============================================================
# FINAL INFORMATION
# ============================================================

print("\n" + "=" * 65)
print("FEATURE DATASET V3 CREATED SUCCESSFULLY!")
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

print("\nMindTrace Feature Extraction V3 completed.")