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
    brand_name = brand_data.get("brand_name", "the brand")
    brand_voice = brand_data.get("brand_voice", [])
    audience = brand_data.get("target_audience", "")
    product = brand_data["products"][product_key]

    preset = presets[preset_key]
    strictness_rule = strictness[strictness_key]

    product_name = product.get("display_name", product_key)
    product_description = product.get("description", "")
    product_benefits = product.get("benefits", [])
    product_claims = product.get("claims", [])
    product_ingredients = product.get("ingredients", [])

    prompt = f"""
You are an expert creative strategist and brand-safe social media copywriter.

Your task is to repurpose an inspiration ad/image into a NEW version for {brand_name}.

====================
BRAND CONTEXT
====================
Brand: {brand_name}
Brand Voice: {", ".join(brand_voice) if isinstance(brand_voice, list) else brand_voice}
Target Audience: {audience}

====================
PRODUCT CONTEXT
====================
Product: {product_name}
Description: {product_description}
Benefits: {", ".join(product_benefits) if product_benefits else "N/A"}
Claims: {", ".join(product_claims) if product_claims else "N/A"}
Ingredients: {", ".join(product_ingredients) if product_ingredients else "N/A"}

====================
CONTENT PRESET
====================
Preset: {preset_key}
Preset Label: {preset.get("label", preset_key)}
Preset Instructions:
{preset.get("instructions", "")}

====================
STRICTNESS RULES
====================
Strictness: {strictness_key}
Strictness Label: {strictness_rule.get("label", strictness_key)}
Rules:
{strictness_rule.get("instructions", "")}

====================
INSPIRATION IMAGE TEXT
====================
{extracted_text}

====================
IMAGE ANALYSIS
====================
{image_analysis}

====================
ADAPTATION LEVEL
====================
{adaptation_level}

====================
OPTIONAL USER NOTES
====================
{optional_text or "None"}

====================
TASK
====================
Create a new ad/campaign concept for this brand based on the inspiration image.

You must:
1. Keep the useful strategic essence of the inspiration.
2. Adapt it strongly to the brand/product.
3. Preserve compliance with strictness rules.
4. Avoid copying wording too closely.
5. Make the final result feel premium, intentional, and brand-native.

Return ONLY the final repurposed creative copy in this exact structure:

HEADLINE:
...

SUBHEAD:
...

BODY:
...

CTA:
...
"""
    return prompt.strip()


def build_final_image_generation_prompt(
    brand_data,
    product_key,
    repurposed_output,
    image_analysis,
    adaptation_level,
    optional_text=None,
):
    """
    Builds the final prompt for AI image generation.
    """
    brand_name = brand_data.get("brand_name", "the brand")
    product = brand_data["products"][product_key]

    product_name = product.get("display_name", product_key)
    product_description = product.get("description", "")
    product_benefits = product.get("benefits", [])

    prompt = f"""
Create a premium high-converting social media advertisement image for {brand_name}.

PRODUCT:
- {product_name}
- {product_description}
- Key benefits: {", ".join(product_benefits) if product_benefits else "N/A"}

REPURPOSED CREATIVE COPY:
{repurposed_output}

INSPIRATION LAYOUT NOTES:
{image_analysis}

ADAPTATION LEVEL:
{adaptation_level}

OPTIONAL USER NOTES:
{optional_text or "None"}

IMAGE GOAL:
- Create a polished, premium, realistic product ad
- Suitable for Instagram feed/post
- Luxury e-commerce style
- Strong visual hierarchy
- Clean spacing
- High-end lighting
- Modern, scroll-stopping composition
- Make it look like a professionally art-directed product campaign

IMPORTANT COMPOSITION RULES:
- Keep layout balanced and uncluttered
- Preserve the inspiration's useful composition principles, but do NOT copy exactly
- Use premium background styling appropriate for the product
- Product should be the clear hero
- Text should be integrated cleanly and be readable
- Include the copy from the repurposed creative in a tasteful ad layout
- Avoid distorted packaging
- Avoid extra fingers/hands unless absolutely necessary
- Avoid low-quality typography
- Avoid random gibberish text
- Ensure the final image looks like a real, premium ad creative

FORMAT:
- Vertical 4:5 composition
- Instagram ad style
- High detail
- Premium commercial product photography
"""
    return prompt.strip()