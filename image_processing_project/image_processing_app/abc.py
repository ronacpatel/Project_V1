import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    text = pytesseract.image_to_string(image_path)
    return text

def extract_date(text):
    date_pattern = r'\d{2}/\d{2}/\d{2}'  # 07/11/23
    date_match = re.search(date_pattern, text)
    if date_match:
        return date_match.group()
    return "not available"

def extract_total_and_subtotal(text):
    total_pattern = r'TOTAL\s*:?[\s\$]*\d+\.\d{2}'  # TOTAL: $112.11 or Total : 79.66 or TOTAL $ 22.62 or TOTAL 110.51
    subtotal_pattern = r'SUBTOTAL\s*:?[\s\$]*\d+\.\d{2}'  # SUBTOTAL: $112.11 or Subtotal : 79.66 or SUBTOTAL $ 22.62 or SUBTOTAL 110.51

    total_matches = re.findall(total_pattern, text, re.IGNORECASE)
    subtotal_matches = re.findall(subtotal_pattern, text, re.IGNORECASE)

    # Last total amount found
    total = total_matches[-1] if total_matches else "not available"

    # Last subtotal amount found
    subtotal = subtotal_matches[-1] if subtotal_matches else "not available"

    return total, subtotal, text
