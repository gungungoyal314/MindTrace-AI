import time
import csv
from datetime import datetime
from pathlib import Path
import pygetwindow as gw


# Project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Raw data folder
RAW_FOLDER = PROJECT_DIR / "data" / "raw"

# Create folder if needed
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

# CSV file
CSV_FILE = RAW_FOLDER / "window_activity.csv"


# Create CSV with headers
if not CSV_FILE.exists():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "active_window"
        ])


def get_active_window():
    try:
        window = gw.getActiveWindow()

        if window is not None:
            return window.title

        return "Unknown"

    except Exception:
        return "Unknown"


def save_data(window_title):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            window_title
        ])


print("🪟 MindTrace Window Tracker Started!")
print("Switch between a few applications for 15 seconds.")
print("Press Ctrl + C to stop.")


last_window = None

try:

    while True:

        current_window = get_active_window()

        # Save only when active window changes
        if current_window != last_window:

            save_data(current_window)

            print(f"Active Window: {current_window}")

            last_window = current_window

        time.sleep(1)

except KeyboardInterrupt:

    print("\n🛑 Window Tracker stopped.")