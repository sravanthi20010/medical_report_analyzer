import pdfplumber
import pytesseract
from PIL import Image

# ✅ FIXED PATH (IMPORTANT)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        else:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img)
    except Exception as e:
        return f"OCR Error: {str(e)}"