from langchain_community.document_loaders.image import UnstructuredImageLoader

from PIL import Image
from io import BytesIO
def extract_text_with_langchain_image(list_dict_final_images):
    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []
    for image_bytes in image_list:
        image = Image.open(BytesIO(image_bytes))
        loader = UnstructuredImageLoader(image)
        docs = loader.load()
        img_text = "\n".join([d.page_content for d in docs])
        image_content.append(img_text)
    return "\n".join(image_content)
from langchain_community.document_loaders  import PyPDFLoader
def extract_text_with_langchain_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    return "\n".join([p.page_content for p in pages])
def full_extraction_pipeline(pdf_path, list_dict_final_images):
    try:
        pdf_text = extract_text_with_langchain_pdf(pdf_path)
    except Exception as e:
        pdf_text = ""
        print("PDF extraction failed:", e)
    try:
        image_text = extract_text_with_langchain_image(list_dict_final_images)
    except Exception as e:
        image_text = ""
        print("Image OCR failed:", e)
    final_output = {
        "pdf_text": pdf_text,
        "image_text": image_text,
        "merged_text": pdf_text + "\n" + image_text
    }
    return final_output
import pickle
class OCRModel:
    def __init__(self):
        pass
    def predict(self, image_or_pdf_path, extra_args=None):
        if extra_args is None:
            extra_args = []
        extracted_text = full_extraction_pipeline(image_or_pdf_path, extra_args)
        return extracted_text
model = OCRModel()
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
