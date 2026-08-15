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
    text: str = Field(..., min_length=3, description="Full article news text to analyze")

class VerifyRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Text snippet or article to search against trusted news sources")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "model_loaded": model_service.is_loaded,
        "service": "AI Fake News Detection API"
    }

async def evaluate_combined_verdict(text: str):
    ml_res = model_service.predict(text)
    
    if ml_res.get("status") == "model_missing":
        raise HTTPException(status_code=400, detail=ml_res.get("error"))

    if ml_res.get("status") == "invalid_input" or ml_res.get("prediction") == "INVALID / NOT A NEWS ARTICLE":
        return {
            "status": "invalid_input",
            "prediction": "INVALID / NOT A NEWS ARTICLE",
            "ml_prediction": "INVALID",
            "confidence": 0.0,
            "category": "N/A",
            "source_verified": False,
            "verified_articles": [],
            "signals": [],
            "reasons": ml_res.get("reasons", ["Input does not match standard news reporting structure."]),
            "disclaimer": "Only factual news reports, press releases, or official circulars can be evaluated for truth verification."
        }

    ml_prediction = ml_res.get("prediction")
    confidence = ml_res.get("confidence", 50.0)
    category = ml_res.get("category", "General")
    signals = ml_res.get("signals", [])

    # Query trusted news API sources
    verify_res = await verify_news_sources(text)
    matches_found = (verify_res.get("status") == "matches_found" and len(verify_res.get("articles", [])) > 0)
    verified_articles = verify_res.get("articles", []) if matches_found else []

    # Final decision rules:
    # REAL condition: ML prediction must be REAL AND trusted-source verification must succeed.
    if ml_prediction == "REAL" and matches_found:
        final_prediction = "REAL"
        source_verified = True
        top_source = verified_articles[0].get("source", "Trusted Source")
        reasons = [
            f"Verified report found from trusted news source ({top_source}).",
            "Logistic Regression ML classifier identified vocabulary patterns consistent with authentic news."
        ]
    elif ml_prediction == "REAL" and not matches_found:
        final_prediction = "FAKE"
        source_verified = False
        reasons = [
            "Logistic Regression ML classifier gave a Real-like structural score, but NO matching report was found across trusted news indices.",
            "Unverified claims or fabricated circulars without trusted source backing are classified as Fake."
        ]
    else:  # ml_prediction == "FAKE"
        final_prediction = "FAKE"
        source_verified = False
        reasons = [
            "Logistic Regression ML classifier identified linguistic patterns strongly associated with Fake/unverified news.",
            "No authentic news verification found across trusted news sources."
        ]

    return {
        "status": "success",
        "prediction": final_prediction,
        "ml_prediction": ml_prediction,
        "confidence": confidence,
        "category": category,
        "source_verified": source_verified,
        "verification_data": verify_res,
        "verified_articles": verified_articles,
        "signals": signals,
        "reasons": reasons,
        "disclaimer": "Final verdict requires both ML classifier structural alignment and live trusted news source verification."
    }

@router.post("/predict/text")
async def predict_text(payload: TextPredictRequest):
    return await evaluate_combined_verdict(payload.text)

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

    eval_res = await evaluate_combined_verdict(extracted_text)

    return {
        "extracted_text": extracted_text,
        "prediction_result": eval_res
    }

@router.post("/verify")
async def verify_source(payload: VerifyRequest):
    res = await verify_news_sources(payload.text)
    return res
