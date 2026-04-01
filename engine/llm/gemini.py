import os
import json
import base64
from io import BytesIO
from PIL import Image
import google.generativeai as genai


class GeminiLLM:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)

        # Text / multimodal analysis model
        self.text_model = genai.GenerativeModel("gemini-2.5-flash")

        # Image generation capable model
        self.image_model_name = "gemini-2.5-flash-image"

    # --------------------
    # Basic text generation
    # --------------------
    def generate(self, prompt: str) -> str:
        response = self.text_model.generate_content(prompt)
        return getattr(response, "text", "").strip()

    # --------------------
    # JSON generation from text
    # --------------------
    def generate_json(self, prompt: str):
        response = self.text_model.generate_content(prompt)
        raw = getattr(response, "text", "").strip()

        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON response:\n{raw}")

    # --------------------
    # Text + image generation (analysis)
    # --------------------
    def generate_with_image(self, prompt: str, uploaded_image) -> str:
        image = Image.open(uploaded_image)

        response = self.text_model.generate_content([
            prompt,
            image
        ])

        return getattr(response, "text", "").strip()

    # --------------------
    # JSON + image generation (analysis)
    # --------------------
    def generate_json_with_image(self, prompt: str, uploaded_image):
        image = Image.open(uploaded_image)

        response = self.text_model.generate_content([
            prompt,
            image
        ])

        raw = getattr(response, "text", "").strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON response from image input:\n{raw}")

    # --------------------
    # Final image generation (prompt only)
    # --------------------
    def generate_image(self, prompt: str):
        image_model = genai.GenerativeModel(self.image_model_name)

        response = image_model.generate_content(prompt)

        pil_image = self._extract_image_from_response(response)

        if pil_image is None:
            raise ValueError(
                "Image generation model did not return an image. "
                "Your Gemini account/model may not support image output with this model name."
            )

        return pil_image

    # --------------------
    # Final image generation (prompt + product reference image)
    # --------------------
    def generate_image_with_reference(self, prompt: str, reference_image_path: str):
        if not reference_image_path:
            raise ValueError("reference_image_path is required")

        if not os.path.exists(reference_image_path):
            raise FileNotFoundError(f"Reference image not found: {reference_image_path}")

        reference_image = Image.open(reference_image_path)

        image_model = genai.GenerativeModel(self.image_model_name)

        response = image_model.generate_content([
            prompt,
            reference_image
        ])

        pil_image = self._extract_image_from_response(response)

        if pil_image is None:
            raise ValueError(
                "Image generation model did not return an image when using reference image. "
                "Your Gemini account/model may not support image output with this model name."
            )

        return pil_image

    # --------------------
    # Internal helper
    # --------------------
    def _extract_image_from_response(self, response):
        # Strategy 1: candidates -> content -> parts
        try:
            for candidate in getattr(response, "candidates", []):
                content = getattr(candidate, "content", None)
                if not content:
                    continue

                for part in getattr(content, "parts", []):
                    inline_data = getattr(part, "inline_data", None)
                    if inline_data and getattr(inline_data, "data", None):
                        image_bytes = inline_data.data
                        return Image.open(BytesIO(image_bytes))

                    data = getattr(part, "data", None)
                    if data:
                        return Image.open(BytesIO(data))
        except Exception:
            pass

        # Strategy 2: response.parts
        try:
            for part in getattr(response, "parts", []):
                inline_data = getattr(part, "inline_data", None)
                if inline_data and getattr(inline_data, "data", None):
                    image_bytes = inline_data.data
                    return Image.open(BytesIO(image_bytes))
        except Exception:
            pass

        # Strategy 3: dict-like fallback
        try:
            response_dict = response.to_dict() if hasattr(response, "to_dict") else None
            if response_dict:
                candidates = response_dict.get("candidates", [])
                for candidate in candidates:
                    content = candidate.get("content", {})
                    for part in content.get("parts", []):
                        inline_data = part.get("inlineData") or part.get("inline_data")
                        if inline_data and inline_data.get("data"):
                            b64 = inline_data["data"]
                            image_bytes = base64.b64decode(b64)
                            return Image.open(BytesIO(image_bytes))
        except Exception:
            pass

        return None