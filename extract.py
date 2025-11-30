import easyocr
from PIL import Image
import numpy as np

reader = easyocr.Reader(['en'])

def extract_fields(image_path):
    image = Image.open(image_path)
    image_np = np.array(image)

    result = reader.readtext(image_np, detail=0)
    text = "\n".join(result)

    extracted_data = {
        "name": "",
        "age": "",
        "diagnosis": ""
    }

    for line in result:
        line_lower = line.lower()
        if "name" in line_lower:
            extracted_data["name"] = line.split(":")[-1].strip()
        if "age" in line_lower:
            extracted_data["age"] = line.split(":")[-1].strip()
        if "diagnosis" in line_lower:
            extracted_data["diagnosis"] = line.split(":")[-1].strip()

    return extracted_data
