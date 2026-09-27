import csv
import time
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk

from pynput import mouse, keyboard
import pygetwindow as gw


# ==========================================
# PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_DIR / "data" / "processed"

DATA_FOLDER.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_FOLDER / "training_data.csv"


# ==========================================
# GLOBAL VARIABLES
# ==========================================

mouse_events = 0
mouse_clicks = 0
keyboard_events = 0

current_label = "unknown"

running = True


# ==========================================
# MOUSE TRACKER
# ==========================================

def on_mouse_move(x, y):
    global mouse_events
    mouse_events += 1


def on_mouse_click(x, y, button, pressed):
    global mouse_events, mouse_clicks

    if pressed:
        mouse_events += 1
        mouse_clicks += 1


# ==========================================
# KEYBOARD TRACKER
# ==========================================

def on_key_press(key):
    global keyboard_events

    # We only count the key.
    # We NEVER save the actual key.
    keyboard_events += 1


# ==========================================
# ACTIVE WINDOW
# ==========================================

def get_active_window():

    try:

        window = gw.getActiveWindow()

        if window is not None:
            title = window.title

            if title:
                return title[:100]

        return "Unknown"

    except Exception:

        return "Unknown"


# ==========================================
# SAVE CURRENT SECOND
# ==========================================

def collect_data():

    global mouse_events
    global mouse_clicks
    global keyboard_events
    global running

    # Create CSV
    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "mouse_events",
            "mouse_clicks",
            "keyboard_events",
            "active_window",
            "attention_label"
        ])

        while running:

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            window = get_active_window()

            writer.writerow([
                timestamp,
                mouse_events,
                mouse_clicks,
                keyboard_events,
                window,
                current_label
            ])

            file.flush()

            # Reset counters for next second
            mouse_events = 0
            mouse_clicks = 0
            keyboard_events = 0

            time.sleep(1)


# ==========================================
# LABEL FUNCTIONS
# ==========================================

def set_label(label):

    global current_label

    current_label = label

    status_label.config(
        text=f"Current state: {label.upper()}"
    )


# ==========================================
# STOP SESSION
# ==========================================

def stop_session():

    global running

    running = False

    root.destroy()


# ==========================================
# START MOUSE LISTENER
# ==========================================

mouse_listener = mouse.Listener(
    on_move=on_mouse_move,
    on_click=on_mouse_click
)

mouse_listener.start()


# ==========================================
# START KEYBOARD LISTENER
# ==========================================

keyboard_listener = keyboard.Listener(
    on_press=on_key_press
)

keyboard_listener.start()


# ==========================================
# START DATA COLLECTION THREAD
# ==========================================

data_thread = threading.Thread(
    target=collect_data,
    daemon=True
)

data_thread.start()


# ==========================================
# GUI
# ==========================================

root = tk.Tk()

root.title("MindTrace AI - Training Session")

root.geometry("600x480")

root.resizable(False, False)


title = tk.Label(
    root,
    text="🧠 MindTrace AI",
    font=("Arial", 26, "bold")
)

title.pack(pady=20)


subtitle = tk.Label(
    root,
    text="Select what you are doing right now",
    font=("Arial", 14)
)

subtitle.pack(pady=5)


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(root)

button_frame.pack(pady=25)


focused_button = tk.Button(
    button_frame,
    text="🟢 FOCUSED",
    width=22,
    height=2,
    command=lambda: set_label("focused")
)

focused_button.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


distracted_button = tk.Button(
    button_frame,
    text="🔴 DISTRACTED",
    width=22,
    height=2,
    command=lambda: set_label("distracted")
)

distracted_button.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


learning_button = tk.Button(
    button_frame,
    text="🔵 LEARNING",
    width=22,
    height=2,
    command=lambda: set_label("learning")
)

learning_button.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


break_button = tk.Button(
    button_frame,
    text="🟡 BREAK",
    width=22,
    height=2,
    command=lambda: set_label("break")
)

break_button.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# ==========================================
# STATUS
# ==========================================

status_label = tk.Label(
    root,
    text="Current state: UNKNOWN",
    font=("Arial", 13, "bold")
)

status_label.pack(pady=15)


info_label = tk.Label(
    root,
    text=(
        "Mouse and keyboard activity are counted only.\n"
        "Actual keyboard keys are never stored."
    ),
    font=("Arial", 10)
)

info_label.pack(pady=10)


stop_button = tk.Button(
    root,
    text="⛔ STOP SESSION",
    width=25,
    height=2,
    command=stop_session
)

stop_button.pack(pady=15)


# ==========================================
# RUN
# ==========================================

print("🧠 MindTrace synchronized training session started.")

root.mainloop()


# ==========================================
# CLEANUP
# ==========================================

running = False

mouse_listener.stop()
keyboard_listener.stop()

print("\n✅ Training session stopped.")

print(f"📁 Dataset saved at:")
print(OUTPUT_FILE)