from dotenv import load_dotenv
from pathlib import Path
import os
import google.generativeai as genai
 
# Load .env from the project root
env_path = Path(__file__).resolve().parent.parent / ".env"
print("Loading:", env_path)
load_dotenv(dotenv_path=env_path)
 
api_key = os.getenv("GOOGLE_API_KEY")
print("Loaded key:", api_key[:6] + "..." if api_key else "No key found")
 
genai.configure(api_key=api_key)
 
model = genai.GenerativeModel("gemini-3-flash-preview")
 
try:
    response = model.generate_content("Say hello in one short sentence.")
    print("\nSUCCESS — key is valid and working.")
    print("Response:", response.text)
except Exception as e:
    print("\nFAILED — key or request is invalid.")
    print("Error type:", type(e).__name__)
    print("Error details:", e)