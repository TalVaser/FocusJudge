import tkinter as tk
from tkinter import messagebox
from judge import get_verdict

current_app = ""

def submit_excuse():
    # getting an explanation from user
    excuse = text_entry.get("1.0", tk.END).strip()

    # no excuse given
    if not (excuse):
        # yes/no window
        surrender = messagebox.askyesno(
            "Appeal Surrendered",
            "You have given up your right to a trial.\nDo you accept the ruling?"
        )

        if surrender:
            print("User surrendered. Activating  DENIED protocol.")
            # will later make user close the site
            root.destroy()
        else:
            return      # returns to excuse window
    else:
        submit_button.config(text="🧑‍⚖️ The Judge is evaluating your case...", state=tk.DISABLED)
        root.update()
        verdict = get_verdict(current_app, excuse)

        if "VERDICT: APPROVED" in verdict:
            messagebox.showinfo("Case Dismissed. You are free to go.", verdict)
        else:
            messagebox.showerror("Guilty! Get back to work!", verdict)

        root.destroy()

def create_court_window(blocked_app_name):
    global root, text_entry,submit_button, current_app

    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    root = tk.Tk()
    root.title("Productivity Court - Access Denied Order")
    root.geometry("800x800")

    # always on top
    root.attributes("-topmost", True)
    root.focus_force()

    root.configure(bg="#ffe3e3")

    title_label = tk.Label(root, text="⛔ACCESS DENIED⛔", font=("Cambria Math", 30, "bold"), bg="#ffe3e3", fg="#b30000")
    title_label.pack(pady=10)

    info_label = tk.Label(root, text=f"Attempted access to: {blocked_app_name}\nPlease justify why this is critical for your work:", font=("Cambria Math", 18), bg="#ffe3e3")
    info_label.pack(pady=5)

    text_entry = tk.Text(root, height=5,width=80, font=("Arial", 12))
    text_entry.pack(pady=5)
    text_entry.focus_set()

    submit_button = tk.Button(root, text="Submit Appeal to The Judge", font=("Cambria Math", 12, "bold"),height=5, width=40, bg="#b30000", fg="white", command=submit_excuse)
    submit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_court_window("YouTube")