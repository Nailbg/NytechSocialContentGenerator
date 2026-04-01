from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import json
import os
import importlib.util
from io import BytesIO
import base64

from engine.generate_caption import generate_caption
from engine.repurpose_content import repurpose_content
from engine.repurpose_image_content import repurpose_image_content
from engine.generate_final_image import generate_final_image
from engine.save_image import save_pil_image
from engine.utils import resolve_product_image_path

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

if not brand_dirs:
    st.error("No brand folders found in /brands")
    st.stop()

brand_key = st.selectbox("Brand", brand_dirs)

# --------------------
# Load brand overview
# --------------------
overview_path = f"brands/{brand_key}/overview.json"
if not os.path.exists(overview_path):
    st.error(f"Missing overview.json for brand: {brand_key}")
    st.stop()

with open(overview_path) as f:
    brand_data = json.load(f)

# --------------------
# Load brand presets dynamically
# --------------------
preset_path = f"brands/{brand_key}/presets.py"
if not os.path.exists(preset_path):
    st.error(f"Missing presets.py for brand: {brand_key}")
    st.stop()

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
# Load strictness dynamically
# --------------------
strictness_path = f"brands/{brand_key}/strictness.py"
if not os.path.exists(strictness_path):
    st.error(f"Missing strictness.py for brand: {brand_key}")
    st.stop()

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
products = brand_data.get("products", {})
if not products:
    st.error("No products found in brand overview.json")
    st.stop()

product_key = st.selectbox(
    "Product",
    list(products.keys()),
    format_func=lambda k: products[k].get("display_name", k)
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
# Helper: auto-download link (best effort)
# --------------------
def auto_download_bytes(file_bytes: bytes, filename: str, mime: str = "image/png"):
    """
    Best-effort browser auto-download using HTML/JS.
    This may work in many local browser sessions, but not guaranteed.
    """
    b64 = base64.b64encode(file_bytes).decode()
    href = f"""
    <a id="download_link" href="data:{mime};base64,{b64}" download="{filename}"></a>
    <script>
        const link = document.getElementById('download_link');
        if (link) {{
            link.click();
        }}
    </script>
    """
    st.components.v1.html(href, height=0)

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
                # Optional: direct check for product reference image before running
                detected_product_ref = resolve_product_image_path(brand_key, product_key)

                if detected_product_ref:
                    st.caption(f"✅ Product reference image found: {detected_product_ref}")
                else:
                    st.caption("⚠️ No product reference image found. Final image will be generated from text only.")

                # Step 1: Analyze and repurpose
                st.info("Step 1/2: Analyzing image and generating repurposed creative...")
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
                    brand_key=brand_key,
                )

                st.success("Creative repurposing complete!")

                st.subheader("Extracted Text")
                st.text_area(
                    "Visible text from inspiration image",
                    result["extracted_text"],
                    height=180
                )

                st.subheader("Image Analysis")
                st.json(result["image_analysis"])

                st.subheader("Repurposed Output")
                st.text_area(
                    "Generated Repurposed Creative",
                    result["repurposed_output"],
                    height=350
                )

                with st.expander("View Final Image Prompt"):
                    st.text_area(
                        "Final Image Prompt",
                        result["final_image_prompt"],
                        height=350
                    )

                # Step 2: Final image generation
                st.info("Step 2/2: Generating final image... this may take longer.")

                product_reference_path = result.get("product_reference_path")

                if product_reference_path:
                    st.caption("🖼️ Using real product reference image for final generation.")
                else:
                    st.caption("📝 No product reference image available. Using prompt-only generation.")

                final_image = generate_final_image(
                    result["final_image_prompt"],
                    product_reference_path=product_reference_path
                )

                # Save permanently
                saved = save_pil_image(
                    final_image,
                    output_dir="generated_images",
                    prefix=f"{brand_key}_{product_key}"
                )

                # Display final image
                st.success(f"Image generated and saved to: {saved['relative_path']}")
                st.subheader("Final Generated Image")
                st.image(final_image, use_container_width=True)

                # Convert to bytes for download
                image_buffer = BytesIO()
                final_image.save(image_buffer, format="PNG")
                image_bytes = image_buffer.getvalue()

                # Reliable manual download button
                st.download_button(
                    label="⬇️ Download Generated Image",
                    data=image_bytes,
                    file_name=saved["filename"],
                    mime="image/png"
                )

                # Best-effort auto-download
                auto_download_enabled = st.checkbox(
                    "Attempt auto-download in browser (best effort)",
                    value=True
                )

                if auto_download_enabled:
                    auto_download_bytes(
                        file_bytes=image_bytes,
                        filename=saved["filename"],
                        mime="image/png"
                    )
                    st.caption("If the browser blocks auto-download, use the download button above.")

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