import json


def build_image_repurpose_prompt(
    brand_data,
    presets,
    preset_key,
    product_key,
    strictness,
    strictness_key,
    extracted_text,
    image_analysis,
    adaptation_level,
    optional_text=None,
):
    preset = presets[preset_key]
    strictness_rule = strictness[strictness_key]
    product_data = brand_data["products"][product_key]

    return f"""
You are a senior brand strategist, direct response copywriter, and creative director.

Your task:
Repurpose a source social media ad/post into a new version for the selected product,
while respecting the selected brand rules and transformation strictness.

BRAND DATA:
{json.dumps(brand_data, indent=2, ensure_ascii=False)}

SELECTED PRESET:
{json.dumps(preset, indent=2, ensure_ascii=False)}

SELECTED PRODUCT:
{json.dumps(product_data, indent=2, ensure_ascii=False)}

STRICTNESS RULE:
{json.dumps(strictness_rule, indent=2, ensure_ascii=False)}

ADAPTATION LEVEL:
{adaptation_level}

OPTIONAL USER NOTES:
{optional_text or ""}

EXTRACTED SOURCE TEXT:
{json.dumps(extracted_text, indent=2, ensure_ascii=False)}

IMAGE ANALYSIS:
{json.dumps(image_analysis, indent=2, ensure_ascii=False)}

TASK:
Create a repurposed creative brief and final copy set for the new product.

You must:
1. Preserve the strongest reusable creative structure from the source image.
2. Replace source-specific claims with product-relevant messaging.
3. Adapt headline, subheadline, CTA, and offer structure for the selected product.
4. Ensure alignment with the brand voice, product truth, and preset style.
5. Respect strictness constraints.

Return ONLY plain text in this exact structure:

=== REPURPOSED CREATIVE BRIEF ===
Hook Strategy:
...
Angle:
...
Visual Direction:
...
What To Keep:
...
What To Replace:
...
What To Adapt:
...
Recommended Layout:
...
Designer Notes:
...

=== FINAL COPY ===
Headline:
...
Subheadline:
...
Body:
...
CTA:
...
Offer / Badge:
...
Disclaimers / Notes:
...
""".strip()