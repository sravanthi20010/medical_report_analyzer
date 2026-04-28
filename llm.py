import requests
import json
import re

def simplify_text(text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",  
                "prompt": f"Simplify this medical report in simple terms:\n{text}",
                "stream": False
            },
            timeout=10  
        )

        data = response.json()
        print("OLLAMA RESPONSE:", data)

        return data.get("response", "No response from model")

    except requests.exceptions.RequestException as e:
        print(f"LLM Error: {str(e)}")
        # Return the original text as fallback
        return text[:500] if len(text) > 500 else text
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return f"LLM Error: {str(e)}"


def extract_structured_data(text):
    """Extract structured medical data directly from medical text using pattern matching"""
    try:
        # Try Ollama first
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": f"""Extract from this medical report and return ONLY valid JSON:
{{"diseases": ["disease1", "disease2"], "medicines": ["medicine1", "medicine2"], "abnormal_values": ["test: value"], "lab_results": {{"name": value}}}}

Medical Report:
{text}""",
                "stream": False
            },
            timeout=10
        )

        response_text = response.json().get("response", "").strip()
        try:
            data = json.loads(response_text)
            if data.get("diseases") or data.get("medicines"):
                return data
        except:
            pass

    except requests.exceptions.RequestException:
        print("Ollama not available, using pattern matching...")
    except Exception as e:
        print(f"Ollama error: {e}")

    # FALLBACK: Extract data using pattern matching from the text
    return extract_structured_data_from_text(text)


def extract_structured_data_from_text(text):
    """Extract medical data using regex patterns"""
    text_lower = text.lower()
    
    # Enhanced disease patterns - more comprehensive
    disease_patterns = [
        'anemia', 'diabetes', 'hypertension', 'cardiac', 'cancer', 'infection', 
        'pneumonia', 'bronchitis', 'asthma', 'tuberculosis', 'hepatitis',
        'arthritis', 'osteoporosis', 'thyroid', 'kidney disease', 'renal',
        'liver disease', 'heart disease', 'stroke', 'angina', 'myopia',
        'hyperlipidemia', 'obesity', 'malnutrition', 'autoimmune',
        'gastritis', 'ulcer', 'colitis', 'crohn', 'ibs', 'leukemia',
        'lymphoma', 'melanoma', 'psoriasis', 'eczema', 'adrenal'
    ]
    
    # Enhanced medicine patterns
    medicine_patterns = [
        'aspirin', 'metformin', 'lisinopril', 'atorvastatin', 'amlodipine',
        'sertraline', 'omeprazole', 'ibuprofen', 'acetaminophen', 'amoxicillin',
        'insulin', 'warfarin', 'clopidogrel', 'simvastatin', 'enalapril',
        'loratadine', 'cetirizine', 'ranitidine', 'famotidine', 'paracetamol',
        'diclofenac', 'metoprolol', 'diltiazem', 'verapamil', 'furosemide',
        'doxycycline', 'ciprofloxacin', 'azithromycin', 'penicillin'
    ]
    
    # Extract diseases
    diseases = []
    for disease in disease_patterns:
        if disease in text_lower:
            diseases.append(disease.title())
    
    # Extract medicines
    medicines = []
    for medicine in medicine_patterns:
        if medicine in text_lower:
            medicines.append(medicine.title())
    
    # Extract lab values using more comprehensive patterns
    abnormal_values = []
    lab_results = {}
    
    # Enhanced patterns for specific lab values
    value_patterns = [
        (r'erythrocytes\s*[:\(]*\s*(\d+\.?\d*)', 'Erythrocytes'),
        (r'hemoglobin\s*[:\(]*\s*(\d+\.?\d*)', 'Hemoglobin'),
        (r'haemoglobin\s*[:\(]*\s*(\d+\.?\d*)', 'Hemoglobin'),
        (r'hb\s+(\d+\.?\d*)', 'Hemoglobin'),
        (r'gmve?\s+(\d+\.?\d*)', 'Hemoglobin (gmve)'),
        (r'wbc\s*[:\(]*\s*(\d+\.?\d*)', 'WBC'),
        (r'leucocytes\s*[:\(]*\s*(\d+\.?\d*)', 'Leucocytes'),
        (r'platelets\s*[:\(]*\s*(\d+\.?\d*)', 'Platelets'),
        (r'glucose\s*[:\(]*\s*(\d+\.?\d*)', 'Glucose'),
        (r'bp\s*[:\(]*\s*(\d+)', 'Blood Pressure'),
        (r'creatinine\s*[:\(]*\s*(\d+\.?\d*)', 'Creatinine'),
        (r'mcv\s*[:\(]*\s*(\d+\.?\d*)', 'MCV'),
        (r'mch\s*[:\(]*\s*(\d+\.?\d*)', 'MCH'),
        (r'mchc\s*[:\(]*\s*(\d+\.?\d*)', 'MCHC'),
        (r'protein\s*[:\(]*\s*(\d+\.?\d*)', 'Protein'),
        (r'albumin\s*[:\(]*\s*(\d+\.?\d*)', 'Albumin'),
    ]
    
    for pattern, label in value_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            try:
                value = float(match.group(1))
                if label not in lab_results:  # Only keep first occurrence
                    lab_results[label] = value
                    abnormal_values.append(f"{label}: {value}")
            except:
                pass
    
    # Look for all numbers followed by units as fallback
    number_patterns = re.findall(r'(\d+\.?\d*)\s*(%|g/dl|g/100ml|mg/dl|bpm|mmhg|units?|/cumm|/cmm|fl|pg)\s*([a-z\s]*)', text, re.IGNORECASE)
    for i, (value, unit, label_text) in enumerate(number_patterns):
        try:
            val = float(value)
            label = label_text.strip()[:25] if label_text.strip() else f"Value {i+1}"
            if val > 0 and val < 100000:  # Reasonable value range
                key = f"{label} ({unit})" if label != f"Value {i+1}" else f"Lab Value {i+1} ({unit})"
                # Check if not already in results
                existing_keys = list(lab_results.keys())
                if key not in existing_keys and len([k for k in existing_keys if unit in k]) < 5:
                    lab_results[key] = val
                    abnormal_values.append(f"{key}: {val}")
        except:
            pass
    
    # If no specific diseases found, look for abnormalities in the report
    if not diseases:
        # For lab reports, extract test names that are mentioned
        test_names = ['hemoglobin', 'erythrocytes', 'leucocytes', 'wbc', 'platelets', 'rbc', 'mcv', 'mch', 'mchc', 'glucose', 'creatinine', 'albumin', 'protein']
        for test in test_names:
            if test in text_lower:
                # Find the corresponding value
                pattern = rf'{test}\s*[:\(]*\s*[^0-9]*(\d+\.?\d*)'
                match = re.search(pattern, text_lower)
                if match:
                    try:
                        val = float(match.group(1))
                        diseases.append(f"{test.title()} - {val}")
                    except:
                        diseases.append(f"{test.title()} (Detected)")
        
        # Also look for abnormality keywords in the text
        abnormality_keywords = ['abnormal', 'elevated', 'low', 'high', 'abnormality', 'disorder', 'disease', 'condition', 'anemia', 'deficiency']
        if any(keyword in text_lower for keyword in abnormality_keywords):
            # Extract lines containing abnormal findings
            for line in text.split('\n'):
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in abnormality_keywords) and len(line.strip()) > 5:
                    cleaned = line.strip()[:80]
                    if cleaned not in diseases:
                        diseases.append(cleaned)
                    if len(diseases) >= 3:
                        break
    
    # If still no medicines found, look for medication indicators
    if not medicines:
        med_indicators = ['medicine', 'drug', 'medication', 'prescribed', 'treatment', 'therapy', 'tablet', 'syrup', 'injection']
        found_med = False
        for line in text.split('\n'):
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in med_indicators):
                cleaned = line.strip()[:80]
                if cleaned not in medicines and len(cleaned) > 3:
                    medicines.append(cleaned)
                    found_med = True
                if len(medicines) >= 2:
                    break
        
        # If no medications found from text, indicate it's a lab report
        if not found_med:
            medicines.append("Lab Report - No medications listed")
    
    return {
        "diseases": diseases if diseases else ["Assessment in progress"],
        "medicines": medicines if medicines else ["No medications specified in report"],
        "abnormal_values": abnormal_values if abnormal_values else ["All standard values extracted"],
        "lab_results": lab_results if lab_results else {"Status": 1}
    }