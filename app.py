import streamlit as st
import json
from engine.generate_caption import generate_brand_caption
import os

st.set_page_config(page_title="Nytech Content Brain", layout="centered")

st.title("🧠 Nytech Content Brain")
st.caption("Turn inspiration into brand-safe content")

# Load available brands
brand_files = os.listdir("brands")
brand_keys = [b.replace(".json", "") for b in brand_files]

# UI Inputs
inspiration = st.text_area("Paste inspiration caption", height=120)

brand_key = st.selectbox("Brand", brand_keys)

# Load products dynamically
with open(f"brands/{brand_key}.json") as f:
    brand_data = json.load(f)

product_key = st.selectbox(
    "Product",
    list(brand_data["products"].keys())
)

boldness = st.selectbox(
    "Boldness",
    ["low", "medium", "high"],
    index=1
)

length = st.selectbox(
    "Length",
    ["short", "medium", "long"],
    index=1
)

generate = st.button("Generate Caption")

if generate and inspiration.strip():
    with st.spinner("Generating..."):
        result = generate_brand_caption(
            inspiration_text=inspiration,
            brand_key=brand_key,
            product_key=product_key,
            boldness=boldness,
            length=length
        )

    st.subheader("Final Caption")
    st.write(result["caption"])

    with st.expander("See analysis"):
        st.json(result["analysis"])
