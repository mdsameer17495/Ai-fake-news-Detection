import os
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_dir(dir_name: str) -> str:
    # 1. Check inside backend directory (e.g. /app/models or backend/models)
    b_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dir_name))
    if os.path.exists(b_dir):
        return b_dir
    # 2. Check project root (e.g. project_root/models)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), dir_name))
    if os.path.exists(root_dir):
        return root_dir
    # 3. Check /app/dir_name in Docker
    docker_dir = os.path.join("/app", dir_name)
    if os.path.exists(docker_dir):
        return docker_dir
    return root_dir

class Settings(BaseSettings):
    APP_NAME: str = "AI Fake News Detection System"
    NEWS_API_KEY: str = ""
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    MODELS_DIR: str = get_dir("models")
    DATA_DIR: str = get_dir("data")
    DB_PATH: str = os.path.join(get_dir("data"), "history.db")
    
    MODEL_PATH: str = os.path.join(MODELS_DIR, "fake_news_model.joblib")
    VECTORIZER_PATH: str = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
    CATEGORY_MODEL_PATH: str = os.path.join(MODELS_DIR, "category_model.joblib")
    CATEGORY_VEC_PATH: str = os.path.join(MODELS_DIR, "category_tfidf.joblib")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
        extra="ignore"
    )

settings = Settings()
