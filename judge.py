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
Your job is to evaluate excuses from a person who was caught trying to open distracting apps (like YouTUbe, Instagram or others they have configured) while they should be focusing on being productive.
The user will provide an excuse.
You must decide if the excuse is genuinely work-related or just a lazy distraction.
Respond with a short, snarky verdict (max 2-3 sentences).
You MUST start your response with either "VERDICT: APPROVED" or "VERDICT: DENIED".
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
        return "VERDICT: DENIED. The court system is down, which automatically makes you guilty. Tough luck. GET BACK TO WORK!"

if __name__ == "__main__":
    test_1 = get_verdict("YouTube", "I need to watch a tutorial on how to center a div in CSS.")
    print(f"\nTest 1: {test_1}")
    print( "-" * 40)

    test_2 = get_verdict("Instagram", "I gotta watch the new drama update")
    print(f"\nTest 2: {test_2}")
