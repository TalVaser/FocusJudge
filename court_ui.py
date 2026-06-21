import customtkinter as ctk
from tkinter import messagebox
import re
from judge import get_verdict

class CourtResult:
    is_approved = False
    approved_minutes = 15

class CourtWindow(ctk.CTkToplevel):
    def __init__(self, blocked_app_name):
        super().__init__()

        self.current_app = blocked_app_name
        CourtResult.is_approved = False
        CourtResult.approved_minutes = 15

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(True)
        except:
            pass

        self.title("Productivity Court - Access Denied")

        self.geometry("550x700")
        self.attributes("-topmost", True)
        self.focus_force()
        self.configure(fg_color="#ffe3e3")

        self.wrapper_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.wrapper_frame.pack(expand=True, fill="both", padx=0, pady=0)

        self.title_label = ctk.CTkLabel(self.wrapper_frame, text="⛔ ACCESS DENIED ⛔", font=("Cambria Math", 28, "bold"), text_color="#b30000")
        self.title_label.pack(pady=(5, 0))


        self.app_label = ctk.CTkLabel(self.wrapper_frame, text=f"Attempted access to: {blocked_app_name}", font=("Cambria Math", 16), text_color="black")
        self.app_label.pack(pady=(15, 0))

        self.justify_label = ctk.CTkLabel(self.wrapper_frame, text="Please justify why this is critical for your work:", font=("Cambria Math", 16), text_color="black")
        self.justify_label.pack(pady=(5, 10))

        self.text_entry = ctk.CTkTextbox(self.wrapper_frame, height=100, width=450, font=("Arial", 14), corner_radius=10, border_width=2, border_color="#b30000", fg_color="white", text_color="black")
        self.text_entry.pack(pady=(0, 15))


        self.time_frame = ctk.CTkFrame(self.wrapper_frame, fg_color="transparent")
        self.time_frame.pack(pady=(0, 15))

        self.time_label = ctk.CTkLabel(self.time_frame, text="Request Grace Period (Minutes):", font=("Arial", 14, "bold"), text_color="black")
        self.time_label.pack(side="left", padx=(0, 10))

        self.time_dropdown = ctk.CTkOptionMenu(self.time_frame, values=["5", "10", "15", "20", "25", "30"], width=80, fg_color="#b30000", button_color="#8a0000", button_hover_color="#5c0000")
        self.time_dropdown.pack(side="left")
        self.time_dropdown.set("15")


        self.submit_button = ctk.CTkButton(self.wrapper_frame, text="Submit Appeal to The Judge", font=("Cambria Math", 16, "bold"), fg_color="#b30000", hover_color="#8a0000", command=self.submit_excuse, height=45, width=450, corner_radius=10)
        self.submit_button.pack(pady=(0, 5))

    def submit_excuse(self):
        excuse = self.text_entry.get("1.0", "end-1c").strip()

        if not excuse:
            surrender = messagebox.askyesno(
                "Appeal Surrendered",
                "You have given up your right to a trial.\nDo you accept the ruling?"
            )

            if surrender:
                print("User surrendered. Activating  DENIED protocol.")
                self.destroy()
            else:
                return
        else:
            self.submit_button.configure(text="The Judge is evaluating your case...", state="disabled")
            self.update()

            requested_mins = self.time_dropdown.get()
            final_excuse = f"{excuse}\n\n[User requests a grace period of {requested_mins} minutes.]"
            verdict = get_verdict(self.current_app, final_excuse)
            self.withdraw()

            if "approved" in verdict.lower():
                CourtResult.is_approved = True
                match = re.search(r"minutes:\s*(\d+)", verdict.lower())
                if match:
                    CourtResult.approved_minutes = int(match.group(1))
                else:
                    CourtResult.approved_minutes = int(requested_mins)

                messagebox.showinfo("Case Dismissed. You are free to go.", verdict)
            else:
                CourtResult.is_approved = False
                messagebox.showerror("Guilty! Get back to work!", verdict)

            self.destroy()

def create_court_window(blocked_app_name):
    return CourtWindow(blocked_app_name)

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    create_court_window("YouTube")
    root.mainloop()