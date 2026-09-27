import csv
import time
from datetime import datetime
from pathlib import Path


# Project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Raw data folder
RAW_FOLDER = PROJECT_DIR / "data" / "raw"

# Session data folder
SESSION_FOLDER = PROJECT_DIR / "data" / "user_sessions"

# Create folders if needed
RAW_FOLDER.mkdir(parents=True, exist_ok=True)
SESSION_FOLDER.mkdir(parents=True, exist_ok=True)

# Output file
SESSION_FILE = SESSION_FOLDER / "current_session.csv"


print("🧠 MindTrace Session Logger")
print("=" * 40)

print("Session started...")
print("Collecting session timeline.")
print("Press Ctrl + C to stop.")

# Create session CSV
with open(SESSION_FILE, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "session_status"
    ])

    start_time = datetime.now()

    try:

        while True:

            current_time = datetime.now()

            writer.writerow([
                current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "active"
            ])

            file.flush()

            print(
                f"Session active: "
                f"{current_time.strftime('%H:%M:%S')}"
            )

            time.sleep(5)

    except KeyboardInterrupt:

        end_time = datetime.now()

        writer.writerow([
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "session_ended"
        ])

        print("\n🛑 Session stopped.")

        duration = end_time - start_time

        print(f"Session duration: {duration}")
        print(f"Data saved to: {SESSION_FILE}")