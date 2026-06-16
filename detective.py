import pygetwindow as gw
import time
from court_ui import create_court_window

# Blacklisted sites - will later change to get from user
BLOCKED_WORDS = ["youtube", "facebook", "instagram", "twitter", "x.com", "whatsapp", "discord", "reddit"]

def watch_windows():
    print("🕵️ Detective is active... scanning windows (Ctrl+C to stop)")

    while True:
        try:
            # Get the currently active window
            active_window = gw.getActiveWindow()

            if active_window is not None:
                title = active_window.title.lower()

                # check if any blocked word is in the window title
                for word in BLOCKED_WORDS:
                    if word in title:
                        print(f"🚨 Distraction detected 🚨 Blocked word: '{word}'. Window title: '{active_window.title}'")
                        active_window.minimize()
                        create_court_window(word.capitalize())

                        print("⏳ Court adjourned. You have 10 seconds to close the distracted tab!")
                        time.sleep(10)

                        break

        except Exception:
            # Ignore momentary errors
            pass

        # Wait to save CPU
        time.sleep(5)


if __name__ == "__main__":
    watch_windows()