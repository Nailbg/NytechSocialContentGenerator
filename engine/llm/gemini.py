import json
import re
import google.generativeai as genai


class GeminiLLM:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def _extract_text(self, response) -> str:
        """
        Defensive text extraction for Gemini responses.
        """
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        try:
            parts = []
            for candidate in getattr(response, "candidates", []):
                content = getattr(candidate, "content", None)
                if not content:
                    continue

                for part in getattr(content, "parts", []):
                    if hasattr(part, "text") and part.text:
                        parts.append(part.text)

            if parts:
                return "\n".join(parts).strip()
        except Exception:
            pass

        return str(response)

    def _clean_json_response(self, text: str) -> str:
        """
        Remove markdown fences if Gemini wraps JSON in ```json ... ```
        """
        text = text.strip()
        text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    def _parse_json_response(self, text: str) -> dict:
        """
        Parse Gemini JSON safely.
        """
        cleaned = self._clean_json_response(text)
        return json.loads(cleaned)

    # ----------------------------
    # TEXT
    # ----------------------------
    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return self._extract_text(response)

    def generate_json(self, prompt: str) -> dict:
        response = self.model.generate_content(prompt)
        text = self._extract_text(response)
        return self._parse_json_response(text)

    # ----------------------------
    # SINGLE IMAGE
    # ----------------------------
    def generate_with_image(
        self,
        prompt: str,
        image_bytes: bytes,
        mime_type: str = "image/png",
    ) -> str:
        response = self.model.generate_content(
            [
                prompt,
                {
                    "mime_type": mime_type,
                    "data": image_bytes,
                },
            ]
        )
        return self._extract_text(response)

    def generate_json_with_image(
        self,
        prompt: str,
        image_bytes: bytes,
        mime_type: str = "image/png",
    ) -> dict:
        response = self.model.generate_content(
            [
                prompt,
                {
                    "mime_type": mime_type,
                    "data": image_bytes,
                },
            ]
        )
        text = self._extract_text(response)
        return self._parse_json_response(text)

    # ----------------------------
    # MULTIPLE IMAGES
    # ----------------------------
    def generate_with_images(self, prompt: str, images: list) -> str:
        """
        images = [
            {"bytes": image_bytes, "mime_type": "image/png"},
            ...
        ]
        """
        parts = [prompt]

        for img in images:
            parts.append(
                {
                    "mime_type": img["mime_type"],
                    "data": img["bytes"],
                }
            )

        response = self.model.generate_content(parts)
        return self._extract_text(response)

    def generate_json_with_images(self, prompt: str, images: list) -> dict:
        """
        images = [
            {"bytes": image_bytes, "mime_type": "image/png"},
            ...
        ]
        """
        parts = [prompt]

        for img in images:
            parts.append(
                {
                    "mime_type": img["mime_type"],
                    "data": img["bytes"],
                }
            )

        response = self.model.generate_content(parts)
        text = self._extract_text(response)
        return self._parse_json_response(text)