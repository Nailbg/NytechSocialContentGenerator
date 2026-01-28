import json
from openai import OpenAI

client = OpenAI()

def generate_brand_caption(
    inspiration_text: str,
    brand_key: str,
    product_key: str,
    platform: str = "instagram",
    boldness: str = "medium",   # low | medium | high
    length: str = "medium"      # short | medium | long
) -> dict:
    """
    Returns:
    {
      "analysis": {...},
      "caption": "final generated caption"
    }
    """

    # 1. Load brand data
    with open(f"brands/{brand_key}/{brand_key}.json") as f:
        brand_data = json.load(f)

    product = brand_data["products"][product_key]

    # 2. Load prompts
    with open("prompts/analyze_inspiration.txt") as f:
        analyze_prompt = f.read()

    with open("prompts/transform_caption.txt") as f:
        transform_prompt = f.read()

    # 3. Analyze inspiration
    analysis_prompt_filled = analyze_prompt.replace(
        "{{CAPTION}}", inspiration_text
    )

    analysis_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON."},
            {"role": "user", "content": analysis_prompt_filled}
        ]
    )

    analysis_json = analysis_response.choices[0].message.content

    # 4. Generate caption
    final_prompt = (
        transform_prompt
        .replace("{{BRAND_JSON}}", json.dumps(brand_data, indent=2))
        .replace("{{PRODUCT_NAME}}", product["display_name"])
        .replace("{{ANALYSIS_JSON}}", analysis_json)
        .replace("{{PLATFORM}}", platform)
        .replace("{{BOLDNESS}}", boldness)
        .replace("{{LENGTH}}", length)
    )

    caption_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You write brand-safe marketing copy."},
            {"role": "user", "content": final_prompt}
        ]
    )

    final_caption = caption_response.choices[0].message.content.strip()

    return {
        "analysis": json.loads(analysis_json),
        "caption": final_caption
    }
