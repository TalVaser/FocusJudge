# Productivity Court 🧑‍⚖️⏳

* "I'll just check Instagram for a second"
* "I'll just answer my Discord dms quickly"
* "Let's watch this tutorial and go back to work without clicking on any other video that will completely waste my time"

NO MORE PROCRASTINATING!

**FocusJudge** - A strict, AI-powered productivity enforcer that acts as your personal judge when you try to access distracting apps. Built with Python, CustomTkinter, and Google's Gemini AI.

## Features
* **Distraction Block:** Blocks predefined distracting websites/apps (like YouTube, Reddit, Instagram).
* **AI Judge:** When a distraction is detected, a court window appears. You must state your case to The Judge! It will Decide if your excuse is good enough to approve.
* **Dynamic Blacklist:** Add or remove apps and websites.
* **Strict System:** The Judge will not let you ignore it until your request is justified.

## Screenshots
<table>
   <tr>
      <td align="center"><img src="https://github.com/user-attachments/assets/357f29fd-3c32-41e7-a96f-db4a9ec706fb" width="280"/><br/><sub><b>Start/Stop Focus</b></sub></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/b8b3beff-323a-4a58-a981-4e5639f39204" width="360"/><br/><sub><b>Explain yourself to The Judge</b></sub></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/5088e3f3-b5e6-48c0-adfe-998d26c6fd49" width="360"/><br/><sub><b>The Verdict!</b></sub></td>
   </tr>
</table>

## How to Use
1. Go to the **Releases** tab on the right side of this page and download the latest `.exe` file.
2. Place the executable in a folder of your choice.
3. In the same folder, create a new text file and name it `.env`.
4. Open the `.env` file and add your Google Gemini API key like this:
   `GEMINI_API_KEY=your_actual_api_key_here`
5. Run the `.exe` and get to work!

## For Developers
1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Set up your API key using `.env.example` as a template.
5. Run `python main.py`.
