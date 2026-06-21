import customtkinter as ctk
from tkinter import messagebox
import time
import pygetwindow as gw
import json
import os
import ctypes
from court_ui import create_court_window
import court_ui

# blacklist settings
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {"blocked_words": ["youtube", "facebook", "instagram", "x.com", "whatsapp", "discord", "reddit"]}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        return DEFAULT_SETTINGS

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


# app UI
class FocusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Productivity Court - Control Panel")
        self.geometry("380x620")

        # load settings
        self.settings = load_settings()
        self.blocked_words = self.settings["blocked_words"]

        self.is_focused = False
        self.start_time = 0
        self.grace_period_until = 0
        self.is_waiting_for_judge = False

        # ------------ design ------------
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        # Reduced vertical padding here to give more room to the bottom
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Focus area
        self.title_label = ctk.CTkLabel(self.main_frame, text="Focus Mode", font=("Cambria Math", 26, "bold"))
        self.title_label.pack(pady=(5, 2))

        self.toggle_btn = ctk.CTkButton(self.main_frame, text="Start Focus", font=("Cambria Math", 18, "bold"),
                                        fg_color="#4CAF50", hover_color="#45a049",
                                        command=self.toggle_focus, width=200, height=45, corner_radius=10)
        self.toggle_btn.pack(pady=(0, 15))

        self.separator = ctk.CTkFrame(self.main_frame, height=2, width=250, fg_color="gray40")
        self.separator.pack(pady=(0, 15))

        # Blacklist management area
        self.settings_label = ctk.CTkLabel(self.main_frame, text="Manage Blocked Apps",
                                           font=("Cambria Math", 14, "bold"))
        self.settings_label.pack(pady=(0, 0))

        self.app_entry = ctk.CTkEntry(self.main_frame, placeholder_text="e.g., netflix, tiktok", width=250, height=35)
        self.app_entry.pack(pady=(0, 10))

        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=(0, 10))

        self.add_btn = ctk.CTkButton(self.btn_frame, text="Add App", command=self.add_app, fg_color="#2196F3",
                                     hover_color="#0b7dda", width=100)
        self.add_btn.pack(side="left", padx=5)

        self.remove_btn = ctk.CTkButton(self.btn_frame, text="Remove", command=self.remove_app, fg_color="#9e9e9e",
                                        hover_color="#757575", width=100)
        self.remove_btn.pack(side="left", padx=5)

        # in-app notifs
        self.status_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12, "bold"), height=15)
        self.status_label.pack(pady=(0, 5))

        # blacklist display
        self.list_title = ctk.CTkLabel(self.main_frame, text="Currently Blocked:", font=("Arial", 12, "bold"))
        self.list_title.pack(pady=(0, 0))

        self.apps_textbox = ctk.CTkTextbox(self.main_frame, width=250, font=("Arial", 14), corner_radius=8,
                                           fg_color="#2b2b2b", text_color="white")
        self.apps_textbox.pack(expand=True, fill="y", pady=(0, 10))
        self.update_list_display()

    # popup message
    def show_status(self, message, color):
        self.status_label.configure(text=message, text_color=color)
        self.after(3000, lambda: self.status_label.configure(text=""))

    # update blacklist
    def update_list_display(self):
        self.apps_textbox.configure(state="normal")
        self.apps_textbox.delete("1.0", "end")
        self.apps_textbox.insert("1.0", "\n".join(sorted(self.blocked_words)))
        self.apps_textbox.configure(state="disabled")

    def add_app(self):
        app_name = self.app_entry.get().strip().lower()
        if app_name:
            if app_name not in self.blocked_words:
                self.blocked_words.append(app_name)
                self.settings["blocked_words"] = self.blocked_words
                save_settings(self.settings)

                self.update_list_display()
                self.show_status(f"Added '{app_name}'", "#4CAF50")
                self.app_entry.delete(0, "end")
            else:
                self.show_status(f"'{app_name}' is already in the blacklist.", "#f44336")

    def remove_app(self):
        app_name = self.app_entry.get().strip().lower()
        if app_name:
            if app_name in self.blocked_words:
                self.blocked_words.remove(app_name)
                self.settings["blocked_words"] = self.blocked_words
                save_settings(self.settings)

                self.update_list_display()
                self.show_status(f"Removed '{app_name}'", "#4caf50")
                self.app_entry.delete(0, "end")
            else:
                self.show_status(f"'{app_name}' is not in the blacklist.", "#f44336")

    def toggle_focus(self):
        if not self.is_focused:
            self.settings = load_settings()
            self.blocked_words = self.settings["blocked_words"]

            self.is_focused = True
            self.start_time = time.time()
            self.grace_period_until = 0
            self.is_waiting_for_judge = False

            self.toggle_btn.configure(text="Stop Focus", fg_color="#f44336", hover_color="#d32f2f")
            print("🕵️ Detective started.")
            self.scan_window()
        else:
            self.is_focused = False
            self.toggle_btn.configure(text="Start Focus", fg_color="#4CAF50", hover_color="#45a049")
            print("Detective stopped.")

            elapsed_time = time.time() - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)

            messagebox.showinfo("Focus Session Ended",
                                f"Great job!\nYou focused for {minutes} minutes and {seconds} seconds.")

    def scan_window(self):
        if not self.is_focused:
            return

        try:
            if not self.is_waiting_for_judge and time.time() >= self.grace_period_until:
                active_window = gw.getActiveWindow()
                if active_window is not None:
                    title = active_window.title.lower()
                    for word in self.blocked_words:
                        if word in title:
                            print(f"🚨Distraction Detected= '{word}'🚨")
                            ctypes.windll.user32.ShowWindow(active_window._hWnd, 6)  # minimize window

                            self.is_waiting_for_judge = True
                            court_win = create_court_window(word.capitalize())
                            self.wait_window(court_win)

                            self.is_waiting_for_judge = False

                            if court_ui.CourtResult.is_approved:
                                mins = court_ui.CourtResult.approved_minutes
                                print(f"Trial won! App is granted {mins} minutes grace period.")

                                self.grace_period_until = time.time() + (mins * 60)
                            else:
                                print("Trial lost! Resuming strict focus. CLOSE DISTRACTION NOW!")
                                self.grace_period_until = time.time() + 10
                            break
        except Exception as e:
            pass

        self.after(1000, self.scan_window)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # dark mode support
    ctk.set_default_color_theme("blue")

    app = FocusApp()
    app.mainloop()