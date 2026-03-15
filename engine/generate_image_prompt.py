# engine/generate_image_prompt.py

def generate_image_prompt(brief, product_data):
    product_name = product_data.get("display_name", "the product")
    visual_notes = product_data.get("visual_notes", "")

    prompt = f"""
Create a polished high-converting social media product advertisement.

Product: {product_name}
Product visual notes: {visual_notes}

Headline concept: {brief['headline']}
Subheadline concept: {brief['subheadline']}
CTA concept: {brief['cta']}

Layout direction:
{brief['layout_plan']}

Visual style:
- Tone: {brief['style_direction']}
- Background: {brief['background_direction']}
- Product placement: {brief['product_placement']}

Requirements:
- Premium commercial advertising quality
- Clean composition
- Strong focal hierarchy
- Brand-safe and realistic product presentation
- Social media ad aesthetic
- 4:5 portrait composition
- Leave room for readable headline and CTA placement
"""
    return prompt.strip()