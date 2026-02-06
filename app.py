from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import json
import os
import importlib.util

from engine.generate_caption import generate_caption

st.set_page_config(page_title="Nytech Content Brain", layout="centered")

st.title("🧠 Nytech Content Brain")
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
# Product selector
# --------------------
product_key = st.selectbox(
    "Product",
    list(brand_data["products"].keys()),
    format_func=lambda k: brand_data["products"][k].get("display_name", k)

)

# --------------------
# Controls
# --------------------
boldness_label = st.selectbox("Boldness", ["low", "medium", "high"], index=1)
length = st.selectbox("Length", ["short", "medium", "long"], index=1)

BOLDNESS_MAP = {
    "low": 3,
    "medium": 5,
    "high": 8
}

inspiration = st.text_area(
    "Paste inspiration caption",
    height=140
)

# --------------------
# Generate
# --------------------
if st.button("Generate Caption") and inspiration.strip():
    with st.spinner("Generating brand-safe content…"):
        result = generate_caption(
            inspiration_text=inspiration,
            brand_data=brand_data,
            presets=PRESETS,
            product_key=product_key,
            preset_key=preset_key,
            boldness=BOLDNESS_MAP[boldness_label],
            length=length
        )

    st.subheader("Final Caption")
    st.write(result)
