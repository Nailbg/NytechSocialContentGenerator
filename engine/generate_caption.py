from engine.config import get_llm
from engine.similarity import is_too_similar
from engine.prompt_builder import build_caption_prompt


def generate_caption(
    source_text,
    brand_data,
    presets,
    product_key,
    preset_key,
    strictness,
    strictness_key,
    length,
    boldness=5,
):
    if preset_key not in presets:
        raise ValueError(f"Preset '{preset_key}' not found for this brand")

    llm = get_llm()

    prompt = build_caption_prompt(
        source_text=source_text,
        brand_data=brand_data,
        presets=presets,          
        preset_key=preset_key,
        product_key=product_key,
        strictness=strictness,  
        strictness_key=strictness_key,  
        boldness=boldness,
        length=length
    )

    output = llm.generate(prompt)

    if is_too_similar(source_text, output):
        raise ValueError("Generated content too similar to inspiration")

    return output
