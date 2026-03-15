def extract_image_text(llm, uploaded_image):
    """
    Extract visible text from an uploaded image using Gemini Vision.
    Returns a structured dict.
    """
    image_bytes = uploaded_image.getvalue()
    mime_type = uploaded_image.type or "image/png"

    prompt = """
You are an expert ad creative analyst.

Task:
Extract ALL visible text from this image as accurately as possible.

Rules:
1. Capture exact wording where possible.
2. Do NOT summarize unless text is unreadable.
3. Group text by likely role:
   - headline
   - subheadline
   - body
   - cta
   - badge_or_offer
   - disclaimer
   - other
4. If text is unclear, include your best guess and mark it as uncertain.
5. Return ONLY valid JSON. No markdown. No explanation.

JSON format:
{
  "headline": [],
  "subheadline": [],
  "body": [],
  "cta": [],
  "badge_or_offer": [],
  "disclaimer": [],
  "other": [],
  "all_text_flat": [],
  "notes": []
}
""".strip()

    return llm.generate_json_with_image(
        prompt=prompt,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )