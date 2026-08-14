import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AI Fake News Detection System"
    NEWS_API_KEY: str = ""
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    DB_PATH: str = os.path.join(BASE_DIR, "data", "history.db")
    
    MODEL_PATH: str = os.path.join(MODELS_DIR, "fake_news_model.joblib")
    VECTORIZER_PATH: str = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
    CATEGORY_MODEL_PATH: str = os.path.join(MODELS_DIR, "category_model.joblib")
    CATEGORY_VEC_PATH: str = os.path.join(MODELS_DIR, "category_tfidf.joblib")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
        extra="ignore"
    )

settings = Settings()
