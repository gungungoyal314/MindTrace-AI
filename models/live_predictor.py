import time
from pathlib import Path

import joblib
import pandas as pd
from pynput import mouse, keyboard


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = PROJECT_DIR / "models" / "attention_model.pkl"


# ============================================================
# LOAD ML MODEL
# ============================================================

if not MODEL_FILE.exists():
    raise FileNotFoundError(
        "attention_model.pkl not found."
    )

model = joblib.load(MODEL_FILE)


# ============================================================
# ACTIVITY COUNTERS
# ============================================================

mouse_events = 0
mouse_clicks = 0
keyboard_events = 0


# ============================================================
# MOUSE TRACKING
# ============================================================

def on_move(x, y):
    global mouse_events
    mouse_events += 1


def on_click(x, y, button, pressed):
    global mouse_events, mouse_clicks

    if pressed:
        mouse_events += 1
        mouse_clicks += 1


# ============================================================
# KEYBOARD TRACKING
# ============================================================

def on_key_press(key):
    global keyboard_events

    # Privacy:
    # Actual keyboard keys are NEVER stored.
    keyboard_events += 1


# ============================================================
# START LISTENERS
# ============================================================

mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click
)

keyboard_listener = keyboard.Listener(
    on_press=on_key_press
)

mouse_listener.start()
keyboard_listener.start()


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("🧠 MINDTRACE AI — LIVE ML PREDICTION")
print("=" * 60)

print("\nModel loaded successfully.")
print("Live prediction started.")
print("Press Ctrl+C to stop.\n")


# ============================================================
# LIVE ML PREDICTION
# ============================================================

try:

    while True:

        # Collect activity for 10 seconds
        time.sleep(10)

        # ----------------------------------------------------
        # Create DataFrame
        # ----------------------------------------------------

        features = pd.DataFrame(
            [[
                mouse_events,
                mouse_clicks,
                keyboard_events
            ]],
            columns=[
                "mouse_events",
                "mouse_clicks",
                "keyboard_events"
            ]
        )

        # ----------------------------------------------------
        # ML Prediction
        # ----------------------------------------------------

        prediction = model.predict(features)[0]

        probabilities = model.predict_proba(features)[0]

        confidence = max(probabilities) * 100

        # ----------------------------------------------------
        # Display Result
        # ----------------------------------------------------

        print("\n" + "-" * 60)

        print(f"🧠 Current State : {prediction}")
        print(f"📊 Confidence   : {confidence:.2f}%")

        print(f"🖱️ Mouse Events  : {mouse_events}")
        print(f"🖱️ Mouse Clicks  : {mouse_clicks}")
        print(f"⌨️ Keyboard     : {keyboard_events}")

        print("-" * 60)

        # ----------------------------------------------------
        # Reset counters for next 10 seconds
        # ----------------------------------------------------

        mouse_events = 0
        mouse_clicks = 0
        keyboard_events = 0


except KeyboardInterrupt:

    print("\n\n🛑 Live prediction stopped.")

    mouse_listener.stop()
    keyboard_listener.stop()