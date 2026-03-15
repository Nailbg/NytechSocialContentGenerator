import json


def analyze_image_layout(llm, uploaded_image, extracted_text, optional_text=None):
    prompt = f"""
You are a senior creative director analyzing an ad creative.

Analyze this image and return a JSON object with the following keys:

{{
  "composition": "Describe overall layout and visual hierarchy",
  "subject_placement": "Where the product/model/main focus is placed",
  "background_style": "Describe background, environment, colors, texture",
  "text_placement": "Where text appears and how it is arranged",
  "design_style": "Overall ad style, e.g. luxury, playful, clinical, minimal, etc.",
  "cta_style": "How CTA is visually presented if any",
  "conversion_elements": "What makes the ad persuasive or attention-grabbing"
}}

Additional context:
Visible extracted text:
{extracted_text}

User notes:
{optional_text or "None"}

Return ONLY valid JSON.
"""
    return llm.generate_json_with_image(prompt, uploaded_image)