def extract_image_text(llm, uploaded_image):
    prompt = """
You are analyzing an advertisement or social media creative.

Extract ALL visible text from the image as accurately as possible.

Rules:
- Preserve line breaks where helpful
- If some text is unclear, make your best guess and mark it with [unclear]
- Return ONLY the extracted text
"""
    return llm.generate_with_image(prompt, uploaded_image)