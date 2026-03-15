# engine/build_creative_brief.py

def build_creative_brief(
    analysis,
    brand_data,
    product_data,
    presets,
    preset_key,
    strictness,
    strictness_key,
    optional_text=None,
    adaptation_level="moderate"
):
    product_name = product_data.get("display_name", "the product")
    benefits = product_data.get("benefits", [])
    primary_benefit = benefits[0] if benefits else "high performance support"

    return {
        "headline": f"Upgrade Your Routine with {product_name}",
        "subheadline": f"Built to deliver {primary_benefit}.",
        "cta": "Shop Now",
        "layout_plan": analysis["reusable_structure"],
        "product_placement": "Hero product centered and clearly visible",
        "background_direction": analysis["visual_style"]["background"],
        "style_direction": analysis["visual_style"]["tone"],
        "adaptation_level": adaptation_level
    }