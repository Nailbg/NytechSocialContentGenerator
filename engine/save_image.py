import os
from datetime import datetime
from pathlib import Path


def save_pil_image(image, output_dir="generated_images", prefix="nytech"):
    """
    Saves a PIL image to disk and returns:
    - absolute path
    - filename
    - relative path
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    relative_path = os.path.join(output_dir, filename)
    absolute_path = os.path.abspath(relative_path)

    image.save(absolute_path, format="PNG")

    return {
        "filename": filename,
        "relative_path": relative_path,
        "absolute_path": absolute_path,
    }