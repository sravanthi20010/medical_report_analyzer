# 🧾 Groq-Based Medical Report Simplification & Clinical Text Analysis

AI-powered medical document analysis system designed to simplify how users understand their health reports. Instead of manually reading complex medical data, the system automates extraction, analysis, and explanation in a user-friendly way.

---

# 1️⃣ Overview

This project is an AI-powered Medical Document Analysis System that uses OCR, document processing, and local Large Language Models powered by Ollama to extract, analyze, and simplify medical reports.
It enables users to upload medical documents, automatically extract key information, and receive clear, patient-friendly explanations along with risk predictions, chatbot support, translation, and voice output.

⭐ **Core Objectives**

• Simplify complex medical report data into easy explanations  
• Extract and process text from medical images/documents  
• Provide AI-generated insights using local LLM (Ollama)  
• Predict potential health risks based on extracted values  
• Enable interactive communication through a chatbot  
• Support multi-language output and voice assistance  
• Ensure privacy by running AI models locally  
• Build a scalable and intelligent healthcare assistant system  

⭐ **Key Features**

✅ Medical Report Upload (Image-Based Input)  
✅ OCR-Based Text Extraction (Report Processing Module)  
✅ AI-Powered Analysis using Ollama (Local LLM)  
✅ Health Risk Prediction Module  
✅ Chatbot Integration for user queries  
✅ Language Translation Support  
✅ Text-to-Speech (Voice Output)  
✅ Clean Flask-Based Web Interface  
✅ Modular Architecture (chatbot, extractor, risk, translate, tts)  
✅ Secure Configuration using (.env)  
✅ Privacy-Focused (Local Processing with Ollama)  
✅ Ready for Deployment  


# 2️⃣ Demos

AI-powered medical document analysis system works like an intelligent healthcare assistant that reads reports and explains them in simple language.

### 🔍 Workflow Demonstration

```
Start
  ↓
User Uploads Medical Report (Image)
  ↓
OCR Module Extracts Text (Extractor)
  ↓
Text Cleaning & Data Processing
  ↓
AI Analysis using Ollama (LLM)
  ↓
Risk Prediction Module
  ↓
+-----------------------------+
| Additional Functionalities  |
|                             |
| → Chatbot Interaction       |
| → Language Translation      |
| → Text-to-Speech Output     |
+-----------------------------+
  ↓
Display Results on Web Interface
  ↓
End
```
# 3️⃣ Project Structure

```
medical-document-ai/
│
├── app.py                     # Main Flask application (entry point)
│
├── templates/                # HTML frontend pages
│   ├── index.html            # Upload interface
│   └── result.html           # Output display page
│
├── static/                   # Static assets (CSS, JS)
│   ├── style.css             # Styling
│   └── script.js             # Frontend logic
│
├── utils/                    # Core backend modules
│   ├── extractor.py          # OCR & text extraction
│   ├── llm.py                # Ollama LLM integration
│   ├── risk.py               # Risk prediction logic
│   ├── chatbot.py            # Chatbot interaction
│   ├── translate.py          # Language translation
│   └── tts.py                # Text-to-Speech
│
├── uploads/                  # Uploaded medical reports
│   └── (images/files)
│
├── report.txt                # Sample processed report/output
├── .env                      # Environment variables (API/config)
└── requirements.txt          # Project dependencies
```

---

# 4️⃣ Run Locally

```

git clone https://github.com/sravanthi20010/medical_report_analyzer.git
cd medical_report_analyzer

pip install -r requirements.txt

python app.py
```


```
http://127.0.0.1:5000
```

---

# 5️⃣ Environment Setup

Create a `.env` file in project root:

```env 
GROQ_API_KEY=your_api_key_here
```

---

# 6️⃣ Deployment Guide

### 1️⃣ Render Deployment

Create new Web Service
Connect GitHub repo
Add environment variable:
GROQ_API_KEY=your_key_here
Start command:
python app.py

---


# 7️⃣ Package Installation Commands

```bash 
pip install flask
pip install easyocr
pip install opencv-python
pip install pillow
pip install numpy
pip install python-dotenv
pip install requests
pip install pyttsx3
pip install googletrans==4.0.0-rc1

```

---

# 8️⃣ Tech Stack

- Python 3.9+  
- Flask  
- Ollama (Local LLM)  
- EasyOCR  
- OpenCV  
- HTML / CSS / JavaScript  
- python-dotenv  
- requests  
- pyttsx3  
- googletrans  

---

# 9️⃣ Conclusion

This project demonstrates the effective use of AI and OCR technologies to simplify and analyze medical reports. By integrating text extraction, data processing, and local AI models using Ollama, the system provides clear, patient-friendly explanations and meaningful health insights.

The inclusion of features such as risk prediction, chatbot interaction, language translation, and text-to-speech enhances usability and accessibility, making medical information easier to understand for users without technical or medical expertise.

Additionally, the use of locally running LLMs ensures data privacy and reduces dependency on external APIs, making the system more secure and scalable. Overall, this project serves as a practical solution for improving healthcare accessibility through intelligent automation.

---

