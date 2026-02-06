import streamlit as st
import requests
import base64

st.set_page_config(page_title="Gemini Image Generator")

st.title("🎨 Gemini Image Generator")

api_key = st.text_input("Gemini API Key", type="password")
prompt = st.text_area("Prompt", placeholder="Describe the image you want")

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.warning("Please provide API key and prompt")
    else:
        with st.spinner("Generating image..."):
            url = (
                "https://generativelanguage.googleapis.com/v1beta/"
                "models/gemini-1.5-pro:generateContent"
                f"?key={api_key}"
            )

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "responseModalities": ["IMAGE"]
                }
            }

            res = requests.post(url, json=payload)
            data = res.json()

            try:
                img_base64 = (
                    data["candidates"][0]["content"]["parts"][0]
                    ["inlineData"]["data"]
                )
                img_bytes = base64.b64decode(img_base64)
                st.image(img_bytes)
            except Exception:
                st.error("Failed to generate image")
                st.json(data)
