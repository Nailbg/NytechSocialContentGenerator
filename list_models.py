# list_models.py
from google import generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyBZfOz6VrGR3B6SVbpL16Bq_pE_RftObbs")

# List all available models
models = genai.list_models()
for m in models:
    print(m)
