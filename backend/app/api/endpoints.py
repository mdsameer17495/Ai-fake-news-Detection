from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
try:
    from app.services.model_service import model_service
    from app.services.ocr_service import extract_text_from_image
    from app.services.verify_service import verify_news_sources
except ModuleNotFoundError:
    from services.model_service import model_service
    from services.ocr_service import extract_text_from_image
    from services.verify_service import verify_news_sources

router = APIRouter()

class TextPredictRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Full article news text to analyze")

class VerifyRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Text snippet or article to search against trusted news sources")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "model_loaded": model_service.is_loaded,
        "service": "AI Fake News Detection API"
    }

@router.post("/predict/text")
def predict_text(payload: TextPredictRequest):
    result = model_service.predict(payload.text)
    
    if result.get("status") in ["model_missing", "invalid_input"]:
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result

@router.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Allowed formats: JPG, JPEG, PNG."
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Image size exceeds the maximum limit of 5 MB."
        )

    ocr_res = extract_text_from_image(contents)
    if not ocr_res["success"]:
        raise HTTPException(status_code=400, detail=ocr_res["error"])

    extracted_text = ocr_res["extracted_text"]

    pred_res = model_service.predict(extracted_text)
    if pred_res.get("status") in ["model_missing", "invalid_input"]:
        raise HTTPException(status_code=400, detail=pred_res.get("error"))

    return {
        "extracted_text": extracted_text,
        "prediction_result": pred_res
    }

@router.post("/verify")
async def verify_source(payload: VerifyRequest):
    res = await verify_news_sources(payload.text)
    return res
