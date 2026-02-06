from engine.config import get_llm
from engine.similarity import is_too_similar
from engine.prompt_builder import build_caption_prompt


def generate_caption(
    inspiration_text,
    brand_data,
    presets,
    product_key,
    preset_key,
    boldness=5,
    length="medium"
):
    if preset_key not in presets:
        raise ValueError(f"Preset '{preset_key}' not found for this brand")

    llm = get_llm()
    preset_data = presets[preset_key]

    prompt = build_caption_prompt(
        inspiration_text=inspiration_text,
        brand_data=brand_data,
        product_key=product_key,
        preset_key=preset_key,
        boldness=boldness,
        length=length
    )

    output = llm.generate(prompt)

    if is_too_similar(inspiration_text, output):
        raise ValueError("Generated content too similar to inspiration")

    return output
