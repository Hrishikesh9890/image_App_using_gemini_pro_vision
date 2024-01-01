from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def generate_text(image_path, custom_prompt):
    # Set up the model
    generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                  generation_config=generation_config)

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_path.read_bytes()
        },
    ]

    prompt_parts = [
        image_parts[0],
        custom_prompt,
    ]

    response = model.generate_content(prompt_parts)
    st.text(response.text)

# Streamlit UI
st.title("Image Application using Gemini Pro Vision")

image_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg"])
custom_prompt = st.text_input("Enter your prompt:")

if st.button("Generate Text"):
    if image_file is not None:
        image_path = Path(image_file.name)
        image_path.write_bytes(image_file.read())
        generate_text(image_path, custom_prompt)
