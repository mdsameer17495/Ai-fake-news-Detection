import os
import io
import shutil
import pytesseract
from PIL import Image

def find_tesseract_cmd() -> str:
    # 1. Check if tesseract is already in PATH
    path_cmd = shutil.which("tesseract")
    if path_cmd and os.path.exists(path_cmd):
        return path_cmd

    # 2. Common Windows installation paths
    windows_candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
        os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe"),
    ]

    for candidate in windows_candidates:
        if os.path.exists(candidate):
            return candidate

    return ""

# Auto-configure pytesseract tesseract_cmd
tesseract_bin = find_tesseract_cmd()
if tesseract_bin:
    pytesseract.pytesseract.tesseract_cmd = tesseract_bin
    print(f"PyTesseract configured with binary: {tesseract_bin}")
else:
    print("Warning: Tesseract OCR binary executable not found in standard paths.")

def extract_text_from_image(image_bytes: bytes) -> dict:
    # Ensure tesseract_cmd is set if discovered
    cmd = pytesseract.pytesseract.tesseract_cmd
    if not cmd or not os.path.exists(cmd):
        # Try rediscovering dynamically
        discovered = find_tesseract_cmd()
        if discovered:
            pytesseract.pytesseract.tesseract_cmd = discovered
            cmd = discovered
        else:
            return {
                "success": False,
                "error": "Tesseract OCR binary engine is not found on the server paths (e.g. C:\\Program Files\\Tesseract-OCR\\tesseract.exe)."
            }

    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert image to RGB mode if required
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")
            
        # Extract text using Hindi + English language configuration (hin+eng) with fallback to eng
        try:
            extracted_text = pytesseract.image_to_string(image, lang="hin+eng").strip()
        except Exception as lang_err:
            print(f"Warning: hin+eng OCR failed ({lang_err}), falling back to eng...")
            extracted_text = pytesseract.image_to_string(image, lang="eng").strip()
        
        if not extracted_text or len(extracted_text.split()) < 2:
            return {
                "success": False,
                "error": "No readable text was detected in this image. Please try a clearer screenshot or article image."
            }
            
        return {
            "success": True,
            "extracted_text": extracted_text
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to process image: {str(e)}"
        }
