import time
import json
from pathlib import Path

import joblib
import pandas as pd
import pygetwindow as gw
from pynput import mouse, keyboard

PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = PROJECT_DIR / "models" / "attention_model.pkl"
LIVE_STATE_FILE = PROJECT_DIR / "data" / "processed" / "live_state.json"
LIVE_HISTORY_FILE = PROJECT_DIR / "data" / "processed" / "live_history.csv"

if not MODEL_FILE.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_FILE}")

model = joblib.load(MODEL_FILE)

mouse_events = 0
mouse_clicks = 0
keyboard_events = 0

def get_window_category(title):
    title = title.lower()
    if "visual studio code" in title or "vs code" in title: return "IDE"
    if "chrome" in title or "edge" in title or "firefox" in title: return "Browser"
    if "youtube" in title or "spotify" in title: return "Entertainment"
    if "instagram" in title: return "Social Media"
    if "whatsapp" in title: return "Messaging"
    if "powerpoint" in title: return "Presentation"
    if "word" in title: return "Document"
    if "excel" in title: return "Spreadsheet"
    if "jupyter" in title: return "Learning / Coding"
    return "Other"

def on_move(x, y):
    global mouse_events
    mouse_events += 1

def on_click(x, y, button, pressed):
    global mouse_events, mouse_clicks
    if pressed:
        mouse_events += 1
        mouse_clicks += 1

def on_key_press(key):
    global keyboard_events
    keyboard_events += 1

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def append_live_history(data):
    LIVE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    row = pd.DataFrame([data])
    header = not LIVE_HISTORY_FILE.exists()
    row.to_csv(LIVE_HISTORY_FILE, mode="a", header=header, index=False)

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener.start()
keyboard_listener.start()

print("=" * 65)
print("🧠 MINDTRACE AI — LIVE ATTENTION ENGINE")
print("=" * 65)
print("✅ ML Model loaded")
print("✅ Mouse tracking started")
print("✅ Keyboard tracking started")
print("✅ Active window tracking started")
print("\n🔐 Privacy Mode:")
print("• Actual keyboard keys are NOT stored")
print("• Raw window titles are NOT stored")
print("\n⏱️ Prediction interval: 10 seconds")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        time.sleep(10)

        active_window = gw.getActiveWindow()
        if active_window:
            window_category = get_window_category(active_window.title.strip())
        else:
            window_category = "Unknown"

        features = pd.DataFrame(
            [[mouse_events, mouse_clicks, keyboard_events]],
            columns=["mouse_events", "mouse_clicks", "keyboard_events"]
        )

        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = max(probabilities) * 100
        timestamp = time.time()

        state = {
            "running": True,
            "timestamp": timestamp,
            "prediction": str(prediction),
            "confidence": round(float(confidence), 2),
            "active_app": window_category,
            "mouse_events": int(mouse_events),
            "mouse_clicks": int(mouse_clicks),
            "keyboard_events": int(keyboard_events)
        }

        write_json(LIVE_STATE_FILE, state)
        append_live_history(state)

        print("\n" + "=" * 65)
        print(f"🧠 Current State : {str(prediction).upper()}")
        print(f"📊 Confidence   : {confidence:.2f}%")
        print(f"🖥️ Active App   : {window_category}")
        print(f"🖱️ Mouse Events : {mouse_events}")
        print(f"🖱️ Mouse Clicks : {mouse_clicks}")
        print(f"⌨️ Keyboard     : {keyboard_events}")
        print("=" * 65)

        mouse_events = 0
        mouse_clicks = 0
        keyboard_events = 0

except KeyboardInterrupt:
    write_json(LIVE_STATE_FILE, {"running": False, "timestamp": time.time()})
    print("\n🛑 MindTrace Live Engine stopped.")
    mouse_listener.stop()
    keyboard_listener.stop()
