import time
from datetime import datetime

from pynput import mouse, keyboard


# ============================================================
# LIVE ACTIVITY COUNTERS
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
    # We only count keyboard activity.
    # Actual keys are NEVER stored.
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
# LIVE MONITOR
# ============================================================

print("=" * 60)
print("🧠 MINDTRACE AI — LIVE ACTIVITY TRACKER")
print("=" * 60)

print("\nTracking started...")
print("Only activity counts are recorded.")
print("Actual keyboard keys are NOT stored.")
print("Press Ctrl+C to stop.\n")


try:

    while True:

        time.sleep(5)

        now = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{now}] "
            f"Mouse: {mouse_events} | "
            f"Clicks: {mouse_clicks} | "
            f"Keyboard: {keyboard_events}"
        )

        # Reset counters every 5 seconds
        mouse_events = 0
        mouse_clicks = 0
        keyboard_events = 0


except KeyboardInterrupt:

    print("\n\n🛑 Live tracking stopped.")

    mouse_listener.stop()
    keyboard_listener.stop()