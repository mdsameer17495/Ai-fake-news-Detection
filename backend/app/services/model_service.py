import os
import re
import joblib
import numpy as np
from app.config import settings

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    # Support Devanagari (Hindi) + Latin (English) characters
    text = re.sub(r'[^\w\s\u0900-\u097F]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

class ModelService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.category_model = None
        self.category_vectorizer = None
        self.is_loaded = False
        self.load_models()

    def load_models(self):
        if os.path.exists(settings.MODEL_PATH) and os.path.exists(settings.VECTORIZER_PATH):
            try:
                self.model = joblib.load(settings.MODEL_PATH)
                self.vectorizer = joblib.load(settings.VECTORIZER_PATH)
                self.is_loaded = True
                print("Successfully loaded fake news model and TF-IDF vectorizer.")
            except Exception as e:
                print(f"Error loading fake news model: {e}")
                self.is_loaded = False
        else:
            print("Model files not found in models/ directory.")
            self.is_loaded = False

        if os.path.exists(settings.CATEGORY_MODEL_PATH) and os.path.exists(settings.CATEGORY_VEC_PATH):
            try:
                self.category_model = joblib.load(settings.CATEGORY_MODEL_PATH)
                self.category_vectorizer = joblib.load(settings.CATEGORY_VEC_PATH)
                print("Successfully loaded category classification model.")
            except Exception as e:
                print(f"Category model not loaded: {e}")

    def predict(self, text: str):
        if not self.is_loaded:
            return {
                "error": "Trained model not found. Please train and place the model files in the models directory.",
                "status": "model_missing"
            }

        cleaned = clean_text(text)
        if not cleaned or len(cleaned.split()) < 3:
            return {
                "error": "Article text is too short or contains insufficient word content for analysis.",
                "status": "invalid_input"
            }

        # Vectorize text
        tfidf_features = self.vectorizer.transform([cleaned])
        
        # Predict class (0 = Fake, 1 = Real)
        prediction_class = self.model.predict(tfidf_features)[0]
        probabilities = self.model.predict_proba(tfidf_features)[0]
        
        prediction_label = "REAL" if prediction_class == 1 else "FAKE"
        confidence = float(probabilities[prediction_class] * 100)

        # Calculate explainability feature influences based on Logistic Regression coefficients & TF-IDF values
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        coefs = self.model.coef_[0]
        
        # Find non-zero feature indices in this input text
        feature_indices = tfidf_features.nonzero()[1]
        
        top_signals = []
        why_reasons = []

        if len(feature_indices) > 0:
            feature_impacts = []
            for idx in feature_indices:
                word = feature_names[idx]
                val = tfidf_features[0, idx]
                coef = coefs[idx]
                score = val * coef  # positive favors REAL, negative favors FAKE
                feature_impacts.append((word, score, coef))
            
            # Sort by absolute impact
            feature_impacts.sort(key=lambda x: abs(x[1]), reverse=True)
            top_signals = [item[0] for item in feature_impacts[:6]]

            if prediction_label == "REAL":
                why_reasons = [
                    "The article contains text patterns commonly associated with Real news in the training data.",
                    f"Key vocabulary signals like '{', '.join(top_signals[:3])}' aligned strongly with verified reporting.",
                    "The overall linguistic structure matches standard informative news patterns learned during model training."
                ]
            else:
                why_reasons = [
                    "The article contains language patterns strongly associated with Fake or misleading news in the training data.",
                    f"Sensational or unverified keyword signals such as '{', '.join(top_signals[:3])}' influenced the classification.",
                    "Several important TF-IDF feature weights deviated from verified news standards."
                ]
        else:
            top_signals = ["general vocabulary"]
            why_reasons = [
                f"The text structure aligns with overall patterns learned for {prediction_label} news.",
                "Model evaluated standard vocabulary frequencies against trained baseline weights."
            ]

        # Category prediction if model available
        predicted_category = "General"
        if self.category_model and self.category_vectorizer:
            try:
                cat_tfidf = self.category_vectorizer.transform([cleaned])
                predicted_category = self.category_model.predict(cat_tfidf)[0]
            except Exception as e:
                print(f"Error predicting category: {e}")

        return {
            "status": "success",
            "prediction": prediction_label,
            "confidence": round(confidence, 1),
            "category": predicted_category,
            "signals": top_signals,
            "reasons": why_reasons,
            "disclaimer": "AI prediction is based on patterns learned from the training data and should not be treated as absolute proof of factual truth."
        }

model_service = ModelService()
