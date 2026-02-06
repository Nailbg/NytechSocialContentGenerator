import google.generativeai as genai
from engine.llm.base import BaseLLM

class GeminiLLM(BaseLLM):
    def __init__(self, model: str, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
