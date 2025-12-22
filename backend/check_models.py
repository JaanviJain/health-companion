import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your password
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("------------------------------------------------")
print("📡 CONNECTING TO GOOGLE TO CHECK MODELS...")
print("------------------------------------------------")

try:
    found = False
    for m in genai.list_models():
        # Only look for models that can write text
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
            found = True
    
    if not found:
        print("❌ Connected, but no text models found. API Key might be restricted.")

except Exception as e:
    print(f"❌ CRASH: {e}")

print("------------------------------------------------")