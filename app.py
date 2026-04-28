from flask import Flask, render_template, request, redirect, send_file
import io
import os
import json

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Rect, String

from utils.chatbot import get_chatbot_response
from utils.extractor import extract_text
from utils.llm import simplify_text, extract_structured_data
from utils.risk import detect_risk
from utils.translate import translate_text, translate_list, translate_lab_results_keys
from utils.tts import speak

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message")

    reply = get_chatbot_response(user_msg)

    return {"reply": reply}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            file = request.files["file"]
            lang = request.form.get("language", "en")

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            print(f"✓ File saved: {path}")

            # Extract text from document
            text = extract_text(path)
            print(f"✓ Text extracted ({len(text)} characters)")
            print(f"First 200 chars: {text[:200]}")
            
            if "Error" in text or "error" in text or len(text) < 10:
                print(f"⚠ Extraction issue: {text}")
                text = f"Medical Document: {file.filename}\nUnable to extract text. Please check file format."
            
            # Simplify text
            simplified = simplify_text(text)
            print(f"✓ Text simplified")
            
            # Detect risk
            risk = detect_risk(text)
            print(f"✓ Risk detected: {risk}")
            
            # Extract structured data (this now uses pattern matching as fallback)
            structured_data = extract_structured_data(text)
            print(f"✓ Structured data extracted: {json.dumps(structured_data, indent=2)}")
            
            diseases = structured_data.get("diseases", [])
            medicines = structured_data.get("medicines", [])
            abnormal_values = structured_data.get("abnormal_values", [])
            lab_results = structured_data.get("lab_results", {})

            translated_simplified = translate_text(simplified, lang)
            translated_diseases = translate_list(diseases, lang)
            translated_medicines = translate_list(medicines, lang)
            translated_abnormal_values = translate_list(abnormal_values, lang)
            translated_lab_results = translate_lab_results_keys(lab_results, lang)

            labels = {
                'risk_assessment': translate_text('Risk assessment', lang),
                'key_findings': translate_text('Key Findings', lang),
                'diseases_found': translate_text('Diseases Detected', lang),
                'medicines': translate_text('Medicines', lang),
                'abnormal_values': translate_text('Abnormal Values', lang),
                'lab_results': translate_text('Lab Results', lang),
                'no_diseases': translate_text('No diseases detected.', lang),
                'no_medicines': translate_text('No medicines found.', lang),
                'no_abnormal_values': translate_text('No abnormal values detected.', lang),
                'no_lab_results': translate_text('No lab results available.', lang)
            }

            return render_template("result.html",
                                   original=text,
                                   simplified=translated_simplified,
                                   labels=labels,
                                   risk=risk,
                                   diseases=translated_diseases,
                                   medicines=translated_medicines,
                                   abnormal_values=translated_abnormal_values,
                                   lab_results=translated_lab_results,
                                   lang=lang)
        
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return render_template("index.html", error=f"Error processing file: {str(e)}")

    return render_template("index.html")


@app.route("/result")
@app.route("/result.html")
def result_redirect():
    return redirect("/")


@app.route("/speak", methods=["POST"])
def speak_route():
    try:
        text = request.form["text"]
        print(f"🔊 Speaking: {text[:100]}...")
        
        # Import here to avoid issues
        import threading
        import time
        
        def speak_async():
            try:
                speak(text)
            except Exception as e:
                print(f"Speech error: {e}")
        
        # Start speech in a separate thread
        speech_thread = threading.Thread(target=speak_async, daemon=True)
        speech_thread.start()
        
        # Return immediately with success message
        return "Speaking results... (Check your speakers)"
        
    except Exception as e:
        print(f"Speak route error: {e}")
        return f"Speech error: {str(e)}"


def build_pdf_report(report_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = styles["Heading2"]
    subheading = styles["Heading3"]
    small = ParagraphStyle("Small", parent=normal, fontSize=10, leading=12)

    story = []
    story.append(Paragraph("MedScan AI Report", styles["Title"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Generated by MedScan AI", ParagraphStyle('Subtitle', parent=normal, fontSize=10, textColor=colors.HexColor('#888888'))))
    story.append(Spacer(1, 16))

    risk_text = report_data.get('risk', 'Unknown')
    risk_upper = risk_text.upper()
    if 'HIGH' in risk_upper:
        risk_color = colors.HexColor('#FF4D4D')
        risk_percent = 90
    elif 'MEDIUM' in risk_upper or 'MODERATE' in risk_upper:
        risk_color = colors.HexColor('#FFB347')
        risk_percent = 60
    else:
        risk_color = colors.HexColor('#00E5C8')
        risk_percent = 25

    story.append(Paragraph("Risk Assessment", heading))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Status: <b>{risk_text}</b>", normal))
    story.append(Spacer(1, 6))

    risk_bar = Drawing(6.0 * inch, 0.35 * inch)
    risk_bar.add(Rect(0, 0, 6.0 * inch, 0.35 * inch, strokeColor=colors.HexColor('#CCCCCC'), fillColor=colors.HexColor('#F5F5F5'), strokeWidth=0.5, rx=4, ry=4))
    risk_bar.add(Rect(0, 0, 6.0 * inch * (risk_percent / 100.0), 0.35 * inch, strokeColor=risk_color, fillColor=risk_color, strokeWidth=0, rx=4, ry=4))
    risk_bar.add(String(3.0 * inch, 0.08 * inch, f"Risk level: {risk_text} ({risk_percent}%)", fillColor=colors.white if risk_percent > 40 else colors.black, fontSize=9, textAnchor='middle'))
    story.append(risk_bar)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Key Findings", heading))
    story.append(Spacer(1, 6))
    story.append(Paragraph(report_data.get('simplified', ''), normal))
    story.append(Spacer(1, 14))

    diseases = report_data.get('diseases', []) or []
    story.append(Paragraph("Diseases Found", subheading))
    if diseases:
        for item in diseases:
            story.append(Paragraph(f"• {item}", normal))
    else:
        story.append(Paragraph(report_data.get('no_diseases', 'No diseases detected.'), normal))
    story.append(Spacer(1, 12))

    medicines = report_data.get('medicines', []) or []
    story.append(Paragraph("Medicines", subheading))
    if medicines:
        for item in medicines:
            story.append(Paragraph(f"• {item}", normal))
    else:
        story.append(Paragraph(report_data.get('no_medicines', 'No medicines found.'), normal))
    story.append(Spacer(1, 12))

    abnormal_values = report_data.get('abnormal_values', []) or []
    story.append(Paragraph("Abnormal Values", subheading))
    if abnormal_values:
        for item in abnormal_values:
            story.append(Paragraph(f"• {item}", normal))
    else:
        story.append(Paragraph(report_data.get('no_abnormal_values', 'No abnormal values detected.'), normal))
    story.append(Spacer(1, 12))

    lab_results = report_data.get('lab_results', {}) or {}
    story.append(Paragraph("Lab Results", subheading))
    if lab_results:
        table_data = [["Test", "Value"]]
        for key, value in lab_results.items():
            table_data.append([str(key), str(value)])
        table = Table(table_data, colWidths=[3.0 * inch, 3.0 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A192F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F7F9FA')),
        ]))
        story.append(table)
    else:
        story.append(Paragraph(report_data.get('no_lab_results', 'No lab results available.'), normal))

    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route("/download", methods=["POST"])
def download():
    report_data_raw = request.form.get("report_data")
    if not report_data_raw:
        return "Missing report data", 400

    try:
        report_data = json.loads(report_data_raw)
    except Exception as e:
        print(f"Download parse error: {e}")
        return "Invalid report data", 400

    pdf_buffer = build_pdf_report(report_data)
    return send_file(pdf_buffer,
                     as_attachment=True,
                     download_name="MedScanAI_Report.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)