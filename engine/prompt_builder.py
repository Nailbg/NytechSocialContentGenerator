# engine/prompt_builder.py

def build_caption_prompt(
    source_text: str,
    brand_data: dict,
    presets: dict,
    product_key: str,
    preset_key: str,
    strictness_key: str,
    strictness: dict,
    boldness: int,
    length: str
):
    if preset_key not in presets:
        raise ValueError(f"Preset '{preset_key}' not found for this brand")
    if strictness_key not in strictness:
        raise ValueError(f"Strictness '{strictness_key}' not found for this brand")

    preset_data = presets[preset_key]
    strictness_data = strictness[strictness_key]
    product = brand_data["products"][product_key]

    voice = brand_data["voice"]
    cta = brand_data["cta_style"]

    if preset_key == "rewrite":
        return f"""
Rewrite the following text for {brand_data['brand']}:
- Keep the original structure, headings, bullets, and paragraphs
- Maintain the flow and style of the original post
- Tailor the text to the brand voice and values
- Mention {product['display_name']} if relevant
====================
TASK
====================
Write an original caption that:
- {strictness_data['instructions']}
- Matches the brand voice and values
- Reflects the product’s benefits naturally
- Feels calm, intentional, and premium
- Uses soft, non-pushy CTAs
- Preserve the original STRUCTURE (paragraphs, bullets, sections)
- Does NOT reuse inspiration phrasing

====================
Preset Instructions: {preset_data["instructions"]}
"""
    else:

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
\"\"\"{source_text}\"\"\"

====================

"""
def build_repurpose_prompt(
    source_text: str,
    brand_data: dict,
    presets: dict,
    product_key: str,
    strictness: dict,
    preset_key: str,
    length: str,
    strictness_key: str
):
    if preset_key not in presets:
        raise ValueError(f"Preset '{preset_key}' not found for this brand")
    if strictness_key not in strictness:
        raise ValueError(f"Strictness '{strictness_key}' not found for this brand")

    preset_data = presets[preset_key]
    strictness_data = strictness[strictness_key]
    product = brand_data["products"][product_key]

    voice = brand_data["voice"]
    cta = brand_data["cta_style"]

    return f"""
Rewrite and repurpose the following content for {brand_data['brand']}.
TASK
====================
Create a repurposed version that:
- {strictness_data['instructions']}
- Maintain the original format in the responses (paragraphs, bullets, sections)
- Feels native to the brand
- Naturally incorporates the product details where relevant
- Matches brand voice and positioning
- Is clearly original and not traceable to the source
- Make length {length}
====================
RULES
====================
- Preserve the original STRUCTURE (paragraphs, bullets, sections)
- Do NOT reuse exact wording or phrasing
- Adapt tone, style, and intent to match the brand
- Naturally adapt the content to feature the selected product
- Keep it original, natural, and platform-ready

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
====================
ORIGINAL CONTENT (STRUCTURE ONLY)
====================
\"\"\"{source_text}\"\"\"
====================


"""
