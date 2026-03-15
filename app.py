from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import json
import os
import importlib.util

from engine.generate_caption import generate_caption
from engine.repurpose_content import repurpose_content
from engine.repurpose_image_content import repurpose_image_content

# --------------------
# Page setup
# --------------------
st.set_page_config(
    page_title="Nytech Content Brain",
    layout="centered"
)

st.title("Nytech Content Generator")
st.caption("Turn inspiration into brand-safe content")

# --------------------
# Load brands
# --------------------
brand_dirs = [
    d for d in os.listdir("brands")
    if os.path.isdir(os.path.join("brands", d))
]

brand_key = st.selectbox("Brand", brand_dirs)

# --------------------
# Load brand overview
# --------------------
with open(f"brands/{brand_key}/overview.json") as f:
    brand_data = json.load(f)

# --------------------
# Load brand presets dynamically
# --------------------
preset_path = f"brands/{brand_key}/presets.py"
preset_spec = importlib.util.spec_from_file_location(
    f"{brand_key}_presets", preset_path
)
presets_module = importlib.util.module_from_spec(preset_spec)
preset_spec.loader.exec_module(presets_module)

PRESETS = presets_module.PRESETS

preset_key = st.selectbox(
    "Content Preset",
    list(PRESETS.keys()),
    format_func=lambda k: PRESETS[k].get("label", k)
)

# --------------------
# Load strictness levels dynamically
# --------------------
strictness_path = f"brands/{brand_key}/strictness.py"
strictness_spec = importlib.util.spec_from_file_location(
    f"{brand_key}_strictness", strictness_path
)
strictness_module = importlib.util.module_from_spec(strictness_spec)
strictness_spec.loader.exec_module(strictness_module)

STRICTNESS = strictness_module.STRICTNESS

strictness_key = st.selectbox(
    "Strictness level",
    list(STRICTNESS.keys()),
    format_func=lambda k: STRICTNESS[k].get("label", k)
)

# --------------------
# Product selector
# --------------------
product_key = st.selectbox(
    "Product",
    list(brand_data["products"].keys()),
    format_func=lambda k: brand_data["products"][k].get("display_name", k)
)

# --------------------
# Mode selector
# --------------------
st.subheader("Content Mode")

mode = st.radio(
    "",
    ["🧩 Repurpose Content", "✍️ Generate Caption", "🖼️ Repurpose Image"],
    horizontal=True
)

MODE_MAP = {
    "🧩 Repurpose Content": "repurpose",
    "✍️ Generate Caption": "caption",
    "🖼️ Repurpose Image": "image"
}

selected_mode = MODE_MAP[mode]

# --------------------
# Shared controls
# --------------------
length = st.selectbox(
    "Length",
    ["identical to original", "shorter than original", "longer than original"],
    index=0
)

BOLDNESS_MAP = {
    "low": 3,
    "medium": 5,
    "high": 8
}

# --------------------
# Mode-specific inputs
# --------------------
inspiration = ""
uploaded_image = None
adaptation_level = None
optional_image_text = None
boldness_label = "medium"

if selected_mode in ["repurpose", "caption"]:
    inspiration = st.text_area(
        "Paste inspiration text",
        height=250,
        placeholder="Paste the text you want to adapt"
    )

if selected_mode == "caption":
    boldness_label = st.selectbox(
        "Boldness",
        ["low", "medium", "high"],
        index=1
    )

if selected_mode == "image":
    adaptation_level = st.selectbox(
        "Adaptation Level",
        ["close match", "moderate", "bold reinterpretation"],
        index=1
    )

    uploaded_image = st.file_uploader(
        "Upload inspiration image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    optional_image_text = st.text_area(
        "Optional inspiration text / notes",
        height=120,
        placeholder="Optional: explain what you like about the image, or paste related copy"
    )

    if uploaded_image is not None:
        st.image(
            uploaded_image,
            caption="Uploaded source creative",
            use_container_width=True
        )

# --------------------
# Generate readiness
# --------------------
can_generate = False

if selected_mode in ["repurpose", "caption"]:
    can_generate = bool(inspiration.strip())
elif selected_mode == "image":
    can_generate = uploaded_image is not None

# --------------------
# Generate button
# --------------------
if st.button("Generate Content", disabled=not can_generate):
    try:
        with st.spinner("Generating..."):

            # --------------------
            # IMAGE MODE
            # --------------------
            if selected_mode == "image":
                result = repurpose_image_content(
                    uploaded_image=uploaded_image,
                    brand_data=brand_data,
                    presets=PRESETS,
                    preset_key=preset_key,
                    product_key=product_key,
                    strictness=STRICTNESS,
                    strictness_key=strictness_key,
                    adaptation_level=adaptation_level,
                    optional_text=optional_image_text,
                )

                st.success("Image repurposing complete!")

                st.subheader("Extracted Text")
                st.json(result["extracted_text"])

                st.subheader("Image Analysis")
                st.json(result["image_analysis"])

                st.subheader("Repurposed Output")
                st.text_area(
                    "Generated Repurposed Creative",
                    result["repurposed_output"],
                    height=500
                )

            # --------------------
            # REPURPOSE TEXT MODE
            # --------------------
            elif selected_mode == "repurpose":
                output = repurpose_content(
                    length=length,
                    source_text=inspiration,
                    brand_data=brand_data,
                    presets=PRESETS,
                    preset_key=preset_key,
                    product_key=product_key,
                    strictness=STRICTNESS,
                    strictness_key=strictness_key,
                )

                st.success("Text repurposing complete!")

                st.text_area(
                    "Generated Content",
                    output,
                    height=500
                )

            # --------------------
            # CAPTION MODE
            # --------------------
            elif selected_mode == "caption":
                output = generate_caption(
                    source_text=inspiration,
                    brand_data=brand_data,
                    presets=PRESETS,
                    preset_key=preset_key,
                    product_key=product_key,
                    strictness=STRICTNESS,
                    strictness_key=strictness_key,
                    boldness=BOLDNESS_MAP[boldness_label],
                )

                st.success("Caption generation complete!")

                st.text_area(
                    "Generated Caption",
                    output,
                    height=400
                )

    except Exception as e:
        st.error(f"Error: {e}")