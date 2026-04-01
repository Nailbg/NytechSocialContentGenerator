import os


def slugify(value: str) -> str:
    return (
        value.lower()
        .replace("&", "and")
        .replace(" ", "_")
        .replace("-", "_")
    )


def resolve_product_asset_path(brand_data, product_key):
    """
    Attempts to locate the product reference image file.

    Expected structure:
    src/brands/[brand_slug]/assets/products/[product_key].png

    Also checks jpg/jpeg/webp variants.
    """
    brand_name = brand_data.get("brand_name", "")
    brand_slug = brand_data.get("brand_slug") or slugify(brand_name)

    possible_extensions = [".png", ".jpg", ".jpeg", ".webp"]

    base_dir = os.path.join(
        "src",
        "brands",
        brand_slug,
        "assets",
        "products"
    )

    for ext in possible_extensions:
        candidate = os.path.join(base_dir, f"{product_key}{ext}")
        if os.path.exists(candidate):
            return candidate

    return None