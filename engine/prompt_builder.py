from engine.presets import PRESETS

def build_caption_prompt(
    inspiration_text,
    brand_data,
    product_key,
    preset,
    boldness,
    length
):
    preset_data = PRESETS[preset]
    product = brand_data["products"][product_key]

    return f"""
Analyze the inspiration content for structure only, not wording.

Brand rules:
- Brand: {brand_data['brand']}
- Tone: {brand_data['tone']}
- Do not use: {brand_data['do_not_use']}
- CTA style: {brand_data['cta_style']}

Product:
- Name: {product_key}
- Benefits: {product['benefits']}
- Positioning: {product['positioning']}

Preset:
- Tone: {preset_data['tone']}
- CTA: {preset_data['cta']}
- Structure: {preset_data['structure']}

Controls:
- Boldness: {boldness}/10
- Length: {length}

Inspiration:
\"\"\"{inspiration_text}\"\"\"

Create original content that follows the structure but uses none of the phrasing.
"""
