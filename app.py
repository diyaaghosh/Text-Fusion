import streamlit as st
import pickle
from pathlib import Path
from ocr_model import OCRModel
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
st.title("OCR Model Test")
uploaded_file = st.file_uploader("Upload a PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
if uploaded_file:
    temp_path = Path("temp_uploaded_file")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
if st.button("Extract Text"):
    with st.spinner("Extracting text..."):
        result = model.predict(temp_path)
        extracted_text = result.get("merged_text", "")
    st.subheader("Extracted Text")
    st.text_area("Output", extracted_text, height=400)

