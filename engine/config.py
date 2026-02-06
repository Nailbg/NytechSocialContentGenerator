import os
from engine.llm.gemini import GeminiLLM

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "gemini")

    if provider == "gemini":
        return GeminiLLM(
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )

    raise ValueError(f"Unsupported provider: {provider}")
