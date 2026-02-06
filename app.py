import streamlit as st
import requests
import base64

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Gemini Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 Gemini Image Generator")

st.caption(
    "Generate images using Google Gemini Vision API "
    "(user provides their own API key)"
)

# ----------------------------
# Inputs
# ----------------------------
api_key = st.text_input(
    "Gemini API Key",
    type="password",
    placeholder="AIza..."
)

prompt = st.text_area(
    "Prompt",
    placeholder="A cinematic photo of a modern tennis racket on a clay court at sunset",
    height=120
)

generate_btn = st.button("Generate Image")

# ----------------------------
# Generate image
# ----------------------------
if generate_btn:
    if not api_key or not prompt:
        st.warning("Please provide both API key and prompt")
    else:
        with st.spinner("Generating image..."):
            url = (
                "https://generativelanguage.googleapis.com/v1beta/"
                "models/gemini-pro-vision:generateContent"
                f"?key={api_key}"
            )

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=60
                )
                result = response.json()

                # ----------------------------
                # Success path (image returned)
                # ----------------------------
                parts = (
                    result.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [])
                )

                image_part = next(
                    (p for p in parts if "inlineData" in p),
                    None
                )

                if image_part:
                    img_base64 = image_part["inlineData"]["data"]
                    img_bytes = base64.b64decode(img_base64)

                    st.success("Image generated successfully")
                    st.image(img_bytes, use_column_width=True)

                    st.download_button(
                        label="Download image",
                        data=img_bytes,
                        file_name="gemini_image.png",
                        mime="image/png"
                    )

                else:
                    st.error("No image returned from Gemini")
                    st.json(result)

            except Exception as e:
                st.error("Request failed")
                st.exception(e)
