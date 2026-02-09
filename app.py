from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import json
import os
import importlib.util

from engine.generate_caption import generate_caption
from engine.repurpose_content import repurpose_content

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
spec = importlib.util.spec_from_file_location(
    f"{brand_key}_presets", preset_path
)
presets_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(presets_module)

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
spec = importlib.util.spec_from_file_location(
    f"{brand_key}_strictness", strictness_path
)
strictness_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(strictness_module)

STRICTNESS = strictness_module.STRICTNESS

# --------------------
# Product selector
# --------------------
product_key = st.selectbox(
    "Product",
    list(brand_data["products"].keys()),
    format_func=lambda k: brand_data["products"][k].get(
        "display_name", k
    )
)
strictness_key = st.selectbox(
    "Strictness level",
    list(STRICTNESS.keys()),
    format_func=lambda k: STRICTNESS[k].get("label", k)
)

# --------------------
# Mode selector (KEY CHANGE)
# --------------------
st.subheader("Content Mode")

mode = st.radio(
    "",
    ["🧩 Repurpose Content", "✍️ Generate Caption"],
    horizontal=True
)

MODE_MAP = {
    "🧩 Repurpose Content": "repurpose",
    "✍️ Generate Caption": "caption"
}

selected_mode = MODE_MAP[mode]

# --------------------
# Controls
# --------------------
if selected_mode == "caption":
    boldness_label = st.selectbox(
        "Boldness",
        ["low", "medium", "high"],
        index=1
    )

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
# Input
# --------------------
inspiration = st.text_area(
    "Paste inspiration text",
    height=250,
    placeholder="Paste the text you want to adapt"
)

# --------------------
# Generate
# --------------------
if st.button("Generate") and inspiration.strip():
    with st.spinner("Generating brand-safe content…"):

        if selected_mode == "repurpose":
            result = repurpose_content(
                length=length,
                source_text=inspiration,
                brand_data=brand_data,
                presets=PRESETS,
                preset_key=preset_key,
                strictness=STRICTNESS,
                strictness_key=strictness_key,
                product_key=product_key,
            )

        else:
            result = generate_caption(
                source_text=inspiration,
                brand_data=brand_data,
                presets=PRESETS,
                product_key=product_key,
                preset_key=preset_key,
                strictness=STRICTNESS,
                strictness_key=strictness_key,
                boldness=BOLDNESS_MAP[boldness_label],
                length=length
            )

    st.subheader("Output")
    st.write(result)
