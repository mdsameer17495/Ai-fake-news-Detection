import os
import io
import shutil
import platform
import pytesseract
from PIL import Image

def find_tesseract_cmd() -> str:
    # 1. Check if tesseract is already in PATH
    path_cmd = shutil.which("tesseract")
    if path_cmd and os.path.exists(path_cmd):
        return path_cmd

    # 2. Common Linux installation paths (Render, Ubuntu, Debian)
    linux_candidates = [
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
    ]

    # 3. Common Windows installation paths
    windows_candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
        os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe"),
    ]

    # Choose candidates based on platform
    if platform.system() == "Windows":
        candidates = windows_candidates + linux_candidates
    else:
        candidates = linux_candidates + windows_candidates

    for candidate in candidates:
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
    if not cmd or (cmd != "tesseract" and not os.path.exists(cmd)):
        # Try rediscovering dynamically
        discovered = find_tesseract_cmd()
        if discovered:
            pytesseract.pytesseract.tesseract_cmd = discovered
            cmd = discovered
        else:
            return {
                "success": False,
                "error": "Tesseract OCR is not installed on this server. Please ensure tesseract-ocr is installed (apt install tesseract-ocr on Linux, or install from https://github.com/UB-Mannheim/tesseract/wiki on Windows)."
            }

    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert image to RGB mode if required
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")
            
        # Extract text using Hindi + English language configuration (hin+eng) with fallbacks
        extracted_text = ""
        try:
            extracted_text = pytesseract.image_to_string(image, lang="hin+eng").strip()
        except Exception as e1:
            print(f"Warning: hin+eng OCR failed ({e1}), trying eng...")
            try:
                extracted_text = pytesseract.image_to_string(image, lang="eng").strip()
            except Exception as e2:
                print(f"Warning: eng OCR failed ({e2}), trying default...")
                try:
                    extracted_text = pytesseract.image_to_string(image).strip()
                except Exception as e3:
                    return {
                        "success": False,
                        "error": f"OCR engine error: {str(e3)}"
                    }
        
        if not extracted_text or len(extracted_text.strip()) == 0:
            return {
                "success": False,
                "error": "No readable text was detected in this image. Please upload a clear image containing news text."
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
