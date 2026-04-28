def detect_risk(text):
    try:
        text = text.lower()

        high_keywords = ["cancer", "tumor", "severe", "critical"]
        medium_keywords = ["infection", "diabetes", "hypertension"]

        if any(word in text for word in high_keywords):
            return "HIGH RISK 🔴"
        elif any(word in text for word in medium_keywords):
            return "MEDIUM RISK 🟠"
        else:
            return "LOW RISK 🟢"
    except Exception as e:
        return f"RISK ANALYSIS ERROR: {str(e)}"