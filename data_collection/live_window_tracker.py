import time
import pygetwindow as gw


# ============================================================
# WINDOW CATEGORY DETECTION
# ============================================================

def get_window_category(title):

    title = title.lower()

    if "visual studio code" in title or "vs code" in title:
        return "IDE"

    if "chrome" in title:
        return "Browser"

    if "edge" in title:
        return "Browser"

    if "firefox" in title:
        return "Browser"

    if "youtube" in title:
        return "Entertainment"

    if "instagram" in title:
        return "Social Media"

    if "whatsapp" in title:
        return "Messaging"

    if "spotify" in title:
        return "Entertainment"

    if "powerpoint" in title:
        return "Presentation"

    if "word" in title:
        return "Document"

    if "excel" in title:
        return "Spreadsheet"

    if "jupyter" in title:
        return "Learning / Coding"

    return "Other"


# ============================================================
# LIVE TRACKING
# ============================================================

print("=" * 60)
print("🧠 MINDTRACE AI — LIVE WINDOW TRACKER")
print("=" * 60)

print("\nTracking active application...")
print("Privacy mode: raw window titles are NOT displayed.")
print("Press Ctrl+C to stop.\n")


last_category = None


try:

    while True:

        active_window = gw.getActiveWindow()

        if active_window:

            title = active_window.title.strip()

            category = get_window_category(title)

            if category != last_category:

                print(
                    f"🖥️ Active Category: {category}"
                )

                last_category = category

        time.sleep(2)


except KeyboardInterrupt:

    print("\n🛑 Window tracking stopped.")