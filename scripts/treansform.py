import json
from openai import OpenAI

client = OpenAI()

BRAND_KEY = "eich"  # change to "a1_supplements", "azharfit", etc.
PRODUCT_KEY = "cocoa_butter"
BOLDNESS = "medium"  # low | medium | high
LENGTH = "medium"   # short | medium | long
MAX_LENGTH = brand_data["platform_defaults"]["instagram"]["max_length"]

with open(f"brands/{BRAND_KEY}/{BRAND_KEY}.json") as f:
    brand_data = json.load(f)

product = brand_data["products"][PRODUCT_KEY]

with open("outputs/analysis.json") as f:
    analysis = f.read()

with open("prompts/transform_caption.txt") as f:
    prompt_template = f.read()

prompt = prompt_template \
    .replace("{{BRAND_JSON}}", json.dumps(brand_data, indent=2)) \
    .replace("{{ANALYSIS_JSON}}", analysis) \
    .replace("{{PRODUCT_NAME}}", product["display_name"]) \
    .replace("{{PLATFORM}}", "Instagram") \
    .replace("{{BOLDNESS}}", BOLDNESS) \
    .replace("{{LENGTH}}", LENGTH)
