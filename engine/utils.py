import re
import os


def clean_json_response(text: str) -> str:
    """
    Remove markdown code fences if Gemini wraps JSON in ```json ... ```
    """
    text = text.strip()

    # Remove opening fence
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)

    # Remove closing fence
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


def resolve_product_image_path(brand_key, product_key):
    """
    Resolves the product reference image path using your actual folder structure:

    brands/{brand_key}/assets/products/{product_key}.png

    Also checks jpg/jpeg/webp.
    Returns the path string if found, otherwise None.
    """
    base_dir = os.path.join("brands", brand_key, "assets", "products")
    extensions = [".png", ".jpg", ".jpeg", ".webp"]

    for ext in extensions:
        candidate = os.path.join(base_dir, f"{product_key}{ext}")
        if os.path.exists(candidate):
            return candidate

    return None