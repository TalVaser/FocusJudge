import tkinter as tk
from tkinter import messagebox
import time
import pygetwindow as gw
from court_ui import create_court_window

# Blacklisted sites - will later change to get from user
BLOCKED_WORDS = ["youtube", "facebook", "instagram", "twitter", "x.com", "whatsapp", "discord", "reddit"]

class FocusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Court - Control Panel")
        self.root.geometry("300x200")
        self.root.configure(bg="#ffe3e3")

        self.is_focused = False
        self.start_time = 0

        self.title_label = tk.Label(root, text="Focus Mode", font=("cambria Math", 20, "bold"), bg="#ffe3e3", fg="#490F1E")
        self.title_label.pack(pady=5)

        self.toggle_btn = tk.Button(root, text="Start Focus", font=("cambria Math", 16, "bold"), bg="#51131F", fg="#ffe3e3", command=self.toggle_focus, width=10, height=3)
        self.toggle_btn.pack(pady=5)

    def toggle_focus(self):
        if not self.is_focused:
            self.is_focused = True
            self.start_time = time.time()
            self.toggle_btn.config(text="Stop Focus", fg="#51131F", bg="#ffe3e3")
            print("🕵️ Detective is active... scanning windows (Ctrl+C to stop)")

            self.scan_windows()
        else:
            self.is_focused = False
            self.toggle_btn.config(text="Start Focus", fg="#ffe3e3", bg="#51131F")
            print("⛔Detective stopped⛔")

            elapsed_time = time.time() - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            messagebox.showinfo("Focus Session Ended",f"Great job!\nSession's length: {minutes} minutes {seconds} seconds")

    def scan_windows(self):
        if not self.is_focused:
            return      # stops scan when button is off

        try:
            active_window = gw.getActiveWindow()
            if active_window is not None:
                title = active_window.title.lower()
                for word in BLOCKED_WORDS:
                    if word in title:
                        print(f"🚨 Distraction detected: '{word}'")
                        active_window.minimize()
                        create_court_window(word.capitalize())      # start court
                        self.root.after(10000, self.scan_windows)
        except Exception:
            pass

        self.root.after(10000, self.scan_windows)

if __name__ == "__main__":
    root = tk.Tk()
    app = FocusApp(root)
    root.mainloop()