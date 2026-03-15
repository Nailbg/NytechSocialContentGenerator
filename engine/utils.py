import re


def clean_json_response(text: str) -> str:
    """
    Remove markdown code fences if Gemini wraps JSON in ```json ... ```
    """
    text = text.strip()

    # Remove opening fence
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)

    # Remove closing fence
    text = re.sub(r"\s*```$", "", text)

    return text.strip()