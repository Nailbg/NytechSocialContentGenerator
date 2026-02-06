# engine/brands.py
import json
from pathlib import Path

BRANDS_DIR = Path(__file__).resolve().parent.parent / "brands"

def load_brand(brand_key: str) -> dict:
    brand_file = BRANDS_DIR / f"{brand_key}.json"

    if not brand_file.exists():
        raise ValueError(f"Brand '{brand_key}' not found in brands/")

    with open(brand_file, "r", encoding="utf-8") as f:
        return json.load(f)
