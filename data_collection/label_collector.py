import csv
from datetime import datetime
from pathlib import Path
import tkinter as tk


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_DIR / "data" / "raw"

DATA_FOLDER.mkdir(parents=True, exist_ok=True)

LABEL_FILE = DATA_FOLDER / "attention_labels.csv"


# ==========================================
# CREATE CSV
# ==========================================

if not LABEL_FILE.exists():

    with open(
        LABEL_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "attention_label"
        ])


# ==========================================
# SAVE LABEL
# ==========================================

def save_label(label):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        LABEL_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            label
        ])

    status_label.config(
        text=f"Saved: {label}  |  {timestamp}"
    )


# ==========================================
# WINDOW
# ==========================================

root = tk.Tk()

root.title("MindTrace - Attention Label Collector")

root.geometry("550x420")

root.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

title = tk.Label(
    root,
    text="🧠 MindTrace AI",
    font=("Arial", 24, "bold")
)

title.pack(pady=20)


subtitle = tk.Label(
    root,
    text="What are you doing right now?",
    font=("Arial", 14)
)

subtitle.pack(pady=10)


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(root)

button_frame.pack(pady=20)


# Focused
focused_button = tk.Button(
    button_frame,
    text="🟢 FOCUSED",
    width=20,
    height=2,
    command=lambda: save_label("focused")
)

focused_button.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


# Distracted
distracted_button = tk.Button(
    button_frame,
    text="🔴 DISTRACTED",
    width=20,
    height=2,
    command=lambda: save_label("distracted")
)

distracted_button.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Learning
learning_button = tk.Button(
    button_frame,
    text="🔵 LEARNING",
    width=20,
    height=2,
    command=lambda: save_label("learning")
)

learning_button.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


# Break
break_button = tk.Button(
    button_frame,
    text="🟡 BREAK",
    width=20,
    height=2,
    command=lambda: save_label("break")
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
    text="No label recorded yet.",
    font=("Arial", 11)
)

status_label.pack(pady=20)


# ==========================================
# INFO
# ==========================================

info = tk.Label(
    root,
    text="Your actual keyboard keys are never stored.",
    font=("Arial", 9)
)

info.pack(pady=5)


# ==========================================
# START APP
# ==========================================

root.mainloop()