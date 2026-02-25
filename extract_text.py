import easyocr
import fitz

reader = easyocr.Reader(['en'])

def extract_from_image(path):
    result = reader.readtext(path)
    return " ".join([r[1] for r in result])

def extract_from_pdf(path):
    text = ""
    pdf = fitz.open(path)
    for page in pdf:
        text += page.get_text()
    return text

def extract_from_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
