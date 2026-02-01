import google.generativeai as genai
import os

# Paste your actual API Key here to test it
api_key = "AIzaSyCJtDJBiBlptf2PZjTmnVk-9sudbXIqCAQ" 
genai.configure(api_key=api_key)

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")