from flask import Flask, render_template, request
from extract_text import extract_from_image, extract_from_pdf, extract_from_txt
from groq_utils import analyze_medical_report
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def parse_output(text):
    def section(name):
        if name + ":" not in text:
            return ""
        return text.split(name + ":")[1].split("\n\n")[0].strip()

    def entity(key):
        for line in text.splitlines():
            if line.startswith(key):
                return line.split(":", 1)[1].strip()
        return ""

    return {
        "patient": section("PATIENT_VIEW"),
        "doctor": section("DOCTOR_VIEW"),
        "entities": {
            "Diseases": entity("Diseases"),
            "Symptoms": entity("Symptoms"),
            "Medicines": entity("Medicines"),
            "Tests": entity("Tests")
        }
    }

@app.route("/", methods=["GET", "POST"])
def home():
    data = None

    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        if file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            text = extract_from_image(filepath)
        elif file.filename.lower().endswith(".pdf"):
            text = extract_from_pdf(filepath)
        else:
            text = extract_from_txt(filepath)

        raw = analyze_medical_report(text)
        print("RAW GROQ OUTPUT:\n", raw)

        data = parse_output(raw)
        print("PARSED DATA:\n", data)

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
