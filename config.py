import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://flask:flask@db:5432/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False