import os
from datetime import datetime


def save_generated_image(image, brand_name: str, product_key: str, output_dir="generated_outputs"):
    """
    Saves a PIL image to disk and returns the saved path.
    """
    safe_brand = (
        brand_name.lower()
        .replace("&", "and")
        .replace(" ", "_")
        .replace("-", "_")
    )

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_brand}_{product_key}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    image.save(filepath, format="PNG")

    return filepath