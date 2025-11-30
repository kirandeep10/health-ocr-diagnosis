import pytesseract
from PIL import Image
import re

# Add your local tesseract path (WINDOWS FIX)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_fields(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))

    fields = {
        "name": None,
        "age": None,
        "weight": None,
        "bp": None,
        "sugar": None,
        "fever": None,
        "heartbeat": None,
        "pulse": None
    }

    # Flexible regex patterns to catch multiple formats
    patterns = {
        "name": r"(Name|Patient Name)[:\- ]+([A-Za-z ]+)",
        "age": r"(Age)[:\- ]+(\d+)",
        "weight": r"(Weight|Wt)[:\- ]+(\d+)",
        "bp": r"(BP|Blood Pressure)[:\- ]+([\d/]+)",
        "sugar": r"(Sugar|Glucose)[:\- ]+(\d+)",
        "fever": r"(Fever|Temp)[:\- ]+(\d+)",
        "heartbeat": r"(Heartbeat|Heart Rate|HR)[:\- ]+(\d+)",
        "pulse": r"(Pulse)[:\- ]+(\d+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[key] = match.group(len(match.groups()))

    return fields


# ------------------------
# Disease Prediction Model
# ------------------------
def predict_disease(data):
    """
    Very simple rule-based prediction
    """

    age = data.get("age")
    weight = data.get("weight")
    bp = data.get("bp")
    sugar = data.get("sugar")
    fever = data.get("fever")
    heartbeat = data.get("heartbeat")
    pulse = data.get("pulse")

    # Add safe conversions
    try: sugar = int(sugar) if sugar else None
    except: sugar = None

    try: fever = int(fever) if fever else None
    except: fever = None

    # Disease Rules
    if sugar and sugar > 180:
        return "⚠️ Possible Diabetes"

    if bp and "/" in bp:
        sys = int(bp.split("/")[0])
        dia = int(bp.split("/")[1])
        if sys > 150 or dia > 95:
            return "⚠️ Possible Hypertension"

    if fever and fever > 100:
        return "🤒 Possible Viral Fever"

    if heartbeat and int(heartbeat) > 110:
        return "❤️ Possible Tachycardia"

    return "✔ No major issues detected"
