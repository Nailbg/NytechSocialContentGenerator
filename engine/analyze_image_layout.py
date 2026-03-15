import json


def analyze_image_layout(llm, uploaded_image, extracted_text=None, optional_text=None):
    """
    Analyze the visual structure, layout, hierarchy, and creative intent
    of the uploaded image using Gemini Vision.
    Returns a structured dict.
    """
    image_bytes = uploaded_image.getvalue()
    mime_type = uploaded_image.type or "image/png"

    extracted_text_str = json.dumps(extracted_text or {}, ensure_ascii=False)
    optional_text_str = optional_text or ""

    prompt = f"""
You are a senior creative strategist and ad designer.

Analyze this social media post / ad image in detail.

Context:
- Extracted text from image: {extracted_text_str}
- Optional user context: {optional_text_str}

Your job:
Analyze the image as a reusable ad template and creative reference.

Return ONLY valid JSON. No markdown. No explanation.

JSON format:
{{
  "creative_type": "",
  "primary_goal": "",
  "funnel_stage": "",
  "audience_impression": "",
  "layout_summary": "",
  "composition": {{
    "focal_point": "",
    "text_placement": "",
    "product_placement": "",
    "negative_space": "",
    "visual_flow": ""
  }},
  "hierarchy": {{
    "first_notice": "",
    "second_notice": "",
    "third_notice": ""
  }},
  "style": {{
    "tone": "",
    "mood": "",
    "color_palette": [],
    "background_type": "",
    "design_style": "",
    "lighting": ""
  }},
  "repurposable_elements": {{
    "keep": [],
    "replace": [],
    "adapt": []
  }},
  "product_integration_recommendation": "",
  "cta_recommendation": "",
  "risks_or_limitations": [],
  "designer_notes": []
}}
""".strip()

    return llm.generate_json_with_image(
        prompt=prompt,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )