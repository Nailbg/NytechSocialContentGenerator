from engine.config import get_llm
from engine.similarity import is_too_similar
from engine.prompt_builder import build_caption_prompt

def generate_caption(
    inspiration_text,
    brand_data,
    product_key,
    preset,
    boldness=5,
    length="medium"
):
    llm = get_llm()

    prompt = build_caption_prompt(
        inspiration_text=inspiration_text,
        brand_data=brand_data,
        product_key=product_key,
        preset=preset,
        boldness=boldness,
        length=length
    )

    output = llm.generate(prompt)

    if is_too_similar(inspiration_text, output):
        raise ValueError("Generated content too similar to inspiration")

    return output
