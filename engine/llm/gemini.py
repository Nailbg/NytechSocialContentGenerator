import google.generativeai as genai


class GeminiLLM:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)

        # ✅ Correct model for v1beta SDK
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)

        # Defensive return (Gemini sometimes returns parts)
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return str(response)
