# list_models.py
import os
from google import generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
# Replace with your actual Gemini API key
genai.configure(api_key)

# List all available models
models = genai.list_models()
for m in models:
    print(m)
