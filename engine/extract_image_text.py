def extract_image_text(llm, uploaded_image):
    prompt = """
You are performing OCR on an advertisement or social media creative.

TASK:
Extract ALL visible text from the image as completely and accurately as possible.

INSTRUCTIONS:
- Capture every readable word, phrase, number, label, headline, subheadline, CTA, badge, disclaimer, and logo text
- Preserve approximate reading order from top to bottom, left to right
- Group text by region if helpful (e.g. HEADLINE, BODY, CTA, PRODUCT LABEL)
- If text is partially unclear, make your best guess and append [unclear]
- If a region clearly contains text but is unreadable, write: [text present but unreadable]
- If there is no visible text, return exactly: NO_VISIBLE_TEXT

RETURN FORMAT:
VISIBLE_TEXT:
...
"""
    return llm.generate_with_image(prompt, uploaded_image)