from engine.config import get_llm


def generate_final_image(final_prompt: str, product_reference_path=None):
    """
    Backward-compatible:
    - If product_reference_path is provided, uses it.
    - Otherwise falls back to prompt-only generation.

    Returns a PIL Image (same as your current app expects).
    """
    llm = get_llm()

    if product_reference_path:
        return llm.generate_image_with_reference(
            prompt=final_prompt,
            reference_image_path=product_reference_path,
        )

    return llm.generate_image(final_prompt)