# Used to test if api key was operational

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Key loaded: {api_key[:5]}... (Length: {len(api_key)})")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash-lite')

try:
    print("Attempting to generate content...")
    response = model.generate_content("Explain 'Hello World' in 5 words.")
    print("\nSUCCESS! API Response:")
    print(response.text)
except Exception as e:
    print(f"\nFAILURE: {e}")