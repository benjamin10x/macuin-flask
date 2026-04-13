import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    API_BASE_URL = os.environ.get("API_BASE_URL") or "http://localhost:8001/api/v1"
    API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "10"))
