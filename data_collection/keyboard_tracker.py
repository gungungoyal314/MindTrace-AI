from pynput import keyboard
from datetime import datetime
import csv
from pathlib import Path


# Project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Raw data folder
RAW_FOLDER = PROJECT_DIR / "data" / "raw"

# Create folder if needed
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

# CSV file
CSV_FILE = RAW_FOLDER / "keyboard_activity.csv"


# Create CSV file with headers
if not CSV_FILE.exists():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "event"
        ])


def save_data(event):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            event
        ])


def on_press(key):

    # We DON'T save the actual key
    save_data("key_pressed")

    print("⌨️ Key pressed")


print("⌨️ MindTrace Keyboard Tracker Started!")
print("Type something for 10 seconds.")
print("Actual keys are NOT being stored.")
print("Press Ctrl + C to stop.")


with keyboard.Listener(
    on_press=on_press
) as listener:

    listener.join()