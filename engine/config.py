import os
from engine.llm.gemini import GeminiLLM


def get_llm():
    provider = os.getenv("LLM_PROVIDER", "gemini")

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        # ✅ No model argument anymore
        return GeminiLLM(api_key=api_key)

    raise ValueError(f"Unsupported LLM provider: {provider}")
