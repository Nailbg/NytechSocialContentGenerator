from engine.config import get_llm
from engine.extract_image_text import extract_image_text
from engine.analyze_image_layout import analyze_image_layout
from engine.image_prompt_builder import build_image_repurpose_prompt


def repurpose_image_content(
    uploaded_image,
    brand_data,
    presets,
    preset_key,
    product_key,
    strictness,
    strictness_key,
    adaptation_level,
    optional_text=None,
):
    # Validate preset
    if preset_key not in presets:
        raise ValueError(f"Preset '{preset_key}' not found for this brand")

    # Validate strictness
    if strictness_key not in strictness:
        raise ValueError(f"Strictness '{strictness_key}' not found for this brand")

    llm = get_llm()

    # Step 1: Extract visible text from image
    extracted_text = extract_image_text(
        llm=llm,
        uploaded_image=uploaded_image,
    )

    # Step 2: Analyze layout / creative structure
    image_analysis = analyze_image_layout(
        llm=llm,
        uploaded_image=uploaded_image,
        extracted_text=extracted_text,
        optional_text=optional_text,
    )

    # Step 3: Build final repurposing prompt
    prompt = build_image_repurpose_prompt(
        brand_data=brand_data,
        presets=presets,
        preset_key=preset_key,
        product_key=product_key,
        strictness=strictness,
        strictness_key=strictness_key,
        extracted_text=extracted_text,
        image_analysis=image_analysis,
        adaptation_level=adaptation_level,
        optional_text=optional_text,
    )

    # Step 4: Generate final repurposed output
    repurposed_output = llm.generate(prompt)

    return {
        "extracted_text": extracted_text,
        "image_analysis": image_analysis,
        "repurposed_output": repurposed_output,
    }