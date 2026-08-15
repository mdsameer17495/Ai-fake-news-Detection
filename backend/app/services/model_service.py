import os
import re
import joblib
import numpy as np
try:
    from app.config import settings
except ModuleNotFoundError:
    from config import settings

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    # Support Devanagari (Hindi) + Latin (English) characters
    text = re.sub(r'[^\w\s\u0900-\u097F]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def is_valid_news_article(text: str) -> tuple[bool, str]:
    if not text or not isinstance(text, str):
        return False, "Input text is empty."

    raw_text = text.strip()
    words = raw_text.split()
    if len(words) < 4:
        return False, "Text is too short to be evaluated as a news article (minimum 4 words required)."

    lower_text = raw_text.lower()

    # 1. Check for conversational / chat / non-news patterns
    conversational_patterns = [
        r'^(i love|i like|i hate|i am|i feel|i think|i want|i need|my name is)\b',
        r'^(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b',
        r'^(how are you|what is|who is|where is|can you|tell me|write a|explain to me)\b',
        r'\b(i love machine learning|i love ai|i like programming|how do you do)\b',
    ]

    news_indicators = [
        'said', 'reported', 'announced', 'according to', 'minister', 'government',
        'police', 'official', 'court', 'university', 'notice', 'circular', 'statement',
        'president', 'pm', 'cm', 'bureau', 'spokesperson', 'dept', 'department',
        'policy', 'bill', 'law', 'press', 'conference', 'source', 'sources'
    ]

    for pattern in conversational_patterns:
        if re.search(pattern, lower_text):
            has_news_kw = any(kw in lower_text for kw in news_indicators)
            if not has_news_kw or len(words) < 15:
                return False, "Input appears to be conversational or casual text rather than a news article."

    # 2. Check for gibberish / repeated character noise
    if re.search(r'(.)\1{4,}', lower_text):
        return False, "Input contains invalid or repeated character noise."

    if re.search(r'\b[bcdfghjklmnpqrstvwxyz]{6,}\b', lower_text):
        return False, "Input contains unrecognized or gibberish character sequences."

    if re.search(r'\b(asdfgh|jklqwerty|zxcvbnm|qwertyuiop)\b', lower_text):
        return False, "Input contains random keyboard pattern gibberish."

    latin_words = [w for w in words if re.match(r'^[a-zA-Z]+$', w)]
    if latin_words:
        total_chars = sum(len(w) for w in latin_words)
        vowels = sum(w.count(v) for w in latin_words for v in 'aeiouy')
        if total_chars >= 10:
            v_ratio = vowels / total_chars
            if v_ratio < 0.12 or v_ratio > 0.65:
                return False, "Input text structure does not resemble natural news reporting sentences."

    return True, ""

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

        is_valid, validation_msg = is_valid_news_article(text)
        if not is_valid:
            return {
                "status": "invalid_input",
                "prediction": "INVALID / NOT A NEWS ARTICLE",
                "confidence": 0.0,
                "category": "N/A",
                "signals": [],
                "reasons": [validation_msg, "The submitted text does not match standard news reporting structure."],
                "error": validation_msg,
                "disclaimer": "Only factual news articles, press releases, or official circulars can be evaluated for truth verification."
            }

        cleaned = clean_text(text)

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
