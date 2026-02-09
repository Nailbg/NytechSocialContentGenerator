from engine.config import get_llm
from engine.prompt_builder import build_repurpose_prompt


def repurpose_content(
    length,
    source_text,
    brand_data,
    presets,
    preset_key,
    product_key,
    strictness,
    strictness_key,
):
    # --------------------
    # Validate preset
    # --------------------
    if preset_key not in presets:
        raise ValueError(f"Preset '{preset_key}' not found for this brand")
    
    if strictness_key not in strictness:
        raise ValueError(f"Strictness '{strictness_key}' not found for this brand")

    llm = get_llm()

    # --------------------
    # Build repurpose prompt
    # --------------------
    prompt = build_repurpose_prompt(
        presets=presets,
        preset_key=preset_key,
        source_text=source_text,
        brand_data=brand_data,
        product_key=product_key,
        strictness=strictness,
        strictness_key=strictness_key,
        length=length,
    )

    # --------------------
    # Generate
    # --------------------
    output = llm.generate(prompt)

    return output
