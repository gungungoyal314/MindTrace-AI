from pynput import mouse
from datetime import datetime
import csv
from pathlib import Path


# Project ka main folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Raw data folder
RAW_FOLDER = PROJECT_DIR / "data" / "raw"

# Folder automatically create karega
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

# CSV file
CSV_FILE = RAW_FOLDER / "mouse_activity.csv"


# Create CSV with headers
if not CSV_FILE.exists():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "event",
            "x",
            "y",
            "button"
        ])


def save_data(event, x, y, button=""):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            event,
            x,
            y,
            button
        ])


def on_move(x, y):

    save_data("move", x, y)

    print(f"Mouse moved: ({x}, {y})")


def on_click(x, y, button, pressed):

    if pressed:

        save_data("click", x, y, str(button))

        print(f"Mouse clicked: ({x}, {y})")


def on_scroll(x, y, dx, dy):

    save_data("scroll", x, y)

    print(f"Mouse scrolled: ({x}, {y})")


print("🖱️ MindTrace Mouse Tracker Started!")
print("Move/click your mouse for a few seconds.")
print("Press Ctrl + C to stop.")


with mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
) as listener:

    listener.join()