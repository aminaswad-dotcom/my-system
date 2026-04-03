import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Parse DATABASE_URL for Render Postgres (or local SQLite with absolute path)
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        elif not db_url.startswith('postgresql://'):
            db_url = 'postgresql://' + db_url.lstrip('/')
    else:
        # Local SQLite with absolute path and auto-create instance/
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, 'instance', 'database.db')
        instance_dir = os.path.join(base_dir, 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        db_url = f'sqlite:///{db_path}'
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads/docs'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    BACKUP_FOLDER = 'backups'
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

    @staticmethod
    def init_folders():
        os.makedirs('static/uploads/docs', exist_ok=True)
        os.makedirs('backups', exist_ok=True)
