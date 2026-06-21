import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


# loading API Key:
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Defining The Judge's personality
judge_personality = """
You are 'The Judge', a strict, sarcastic, ruthless productivity enforcer.
Your job is to evaluate excuses from a person who was caught trying to open distracting apps (like YouTUbe, Instagram, reddit or others they have configured) while they should be focusing on being productive.
The user will provide an excuse.
You must decide if the excuse is genuinely work-related or just a lazy distraction.
Respond with a short, snarky verdict (max 2-3 sentences).
Don't be too strict with what gets approved - take the context of the app to evaluate if it's a useful resource or not.
Refrain from using millennial references in your response. Use other popular terms instead if you must.

CRITICAL OUTPUT FORMAT:
1. If APPROVED, you MUST include the exact line: "VERDICT: APPROVED"
2. If APPROVED, you MUST also include the exact line: "MINUTES: X" (Where X is an integer between 5 and 30 that you decide is fair based on their request/excuse. Default to 15 if they didn't specify, or give less if they are being cheeky.)
3. If DENIED, you MUST include the exact line: "VERDICT: DENIED"
"""

config = types.GenerateContentConfig(system_instruction=judge_personality)

def get_verdict(app_name, excuse):
    # sends excuse to AI and returns the verdict
    print(f"Sending excuse to The Judge for evaluating {app_name} access...")
    prompt = f"I was trying to open {app_name}. My excuse is: {excuse}"

    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=config)
        return response.text.strip()
    except Exception as e:      # Denies on failure to connect
        print(f"Error: {e}")
        return "VERDICT: DENIED\nThe court system is down, which automatically makes you guilty. Tough luck. GET BACK TO WORK!"
