import os

# ---- Provider selection ----
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

# ---- Model config ----
MODELS = {
    "gemini": {
        "text": "gemini-2.5-flash",
        "image": "nano-banana-pro"
    },
    "openai": {
        "text": "gpt-4o-mini",
        "image": "gpt-image-1"
    }
}

# ---- Generation defaults ----
DEFAULTS = {
    "temperature": 0.7,
    "max_output_tokens": 500
}
