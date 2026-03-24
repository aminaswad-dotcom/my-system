import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads/docs'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    BACKUP_FOLDER = 'backups'
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

    @staticmethod
    def init_folders():
        os.makedirs('static/uploads/docs', exist_ok=True)
        os.makedirs('backups', exist_ok=True)
