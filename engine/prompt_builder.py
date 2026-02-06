# engine/prompt_builder.py

from brands.eich.presets import PRESETS

def build_caption_prompt(
    inspiration_text: str,
    brand_data: dict,
    product_key: str,
    preset_key: str,
    boldness: int,
    length: str
):
    preset_data = PRESETS[preset_key]
    product = brand_data["products"][product_key]

    voice = brand_data["voice"]
    cta = brand_data["cta_style"]

    return f"""
Analyze the inspiration content for STRUCTURE only.
Do NOT reuse wording, phrasing, or sentence patterns.

====================
BRAND IDENTITY
====================
Brand: {brand_data['brand']}
Tagline: {brand_data.get('tagline')}

Brand Voice:
- Tone: {", ".join(voice['tone'])}
- Style: {", ".join(voice['style'])}
- Personality: {", ".join(voice['personality'])}
- Avoid Tone: {", ".join(voice['avoid_tone'])}

Messaging Pillars:
- {", ".join(brand_data['messaging_pillars'])}

Forbidden Language:
- {", ".join(brand_data['do_not_use'])}

CTA Style:
- Type: {cta['primary']}
- Example CTAs: {", ".join(cta['examples'])}

====================
PRODUCT CONTEXT
====================
Product Name: {product['display_name']}
Category: {product['category']}
Positioning: {product['positioning']}

Key Benefits:
- {", ".join(product['benefits'])}

Sensory Notes:
- Texture: {product['sensory_notes'].get('texture')}
- Fragrance: {product['sensory_notes'].get('fragrance')}

====================
CONTENT PRESET
====================
Preset Name: {preset_data['label']}
Tone Direction: {preset_data['tone']}
CTA Direction: {preset_data['cta']}
Structure Guide: {preset_data['structure']}

====================
CREATIVE CONTROLS
====================
Boldness Level: {boldness}/10
Length: {length}

====================
INSPIRATION (STRUCTURE ONLY)
====================
\"\"\"{inspiration_text}\"\"\"

====================
TASK
====================
Write an original caption that:
- Matches the brand voice and values
- Reflects the product’s benefits naturally
- Feels calm, intentional, and premium
- Uses soft, non-pushy CTAs
- Does NOT reuse inspiration phrasing
"""
