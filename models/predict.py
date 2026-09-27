import time
import joblib
from pathlib import Path
from pynput import mouse, keyboard


# ==========================================
# PROJECT PATH
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = PROJECT_DIR / "models" / "attention_model.pkl"


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(MODEL_FILE)

print("🧠 MindTrace Attention Predictor")
print("=" * 40)
print("Model loaded successfully!")
print("Monitoring your activity...")
print("Press Ctrl + C to stop.\n")


# ==========================================
# ACTIVITY COUNTERS
# ==========================================

mouse_events = 0
mouse_clicks = 0
keyboard_events = 0


# ==========================================
# MOUSE
# ==========================================

def on_mouse_move(x, y):

    global mouse_events

    mouse_events += 1


def on_mouse_click(x, y, button, pressed):

    global mouse_events
    global mouse_clicks

    if pressed:

        mouse_events += 1
        mouse_clicks += 1


# ==========================================
# KEYBOARD
# ==========================================

def on_key_press(key):

    global keyboard_events

    keyboard_events += 1


# ==========================================
# START LISTENERS
# ==========================================

mouse_listener = mouse.Listener(
    on_move=on_mouse_move,
    on_click=on_mouse_click
)

keyboard_listener = keyboard.Listener(
    on_press=on_key_press
)

mouse_listener.start()
keyboard_listener.start()


# ==========================================
# REAL-TIME LOOP
# ==========================================

try:

    while True:

        # Wait 10 seconds
        time.sleep(10)

        # Create feature vector
        features = [[
            mouse_events,
            mouse_clicks,
            keyboard_events
        ]]

        # Predict
        prediction = model.predict(
            features
        )[0]

        # Probability
        probabilities = model.predict_proba(
            features
        )[0]

        confidence = max(
            probabilities
        ) * 100

        print(
            f"🧠 Prediction: "
            f"{prediction.upper()}"
        )

        print(
            f"📊 Confidence: "
            f"{confidence:.2f}%"
        )

        print(
            f"🖱️ Mouse events: "
            f"{mouse_events}"
        )

        print(
            f"⌨️ Keyboard events: "
            f"{keyboard_events}"
        )

        print("-" * 40)

        # Reset counters
        mouse_events = 0
        mouse_clicks = 0
        keyboard_events = 0


except KeyboardInterrupt:

    print("\n🛑 Predictor stopped.")

    mouse_listener.stop()
    keyboard_listener.stop()