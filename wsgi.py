import sys
import os
# Add project path for imports
sys.path.insert(0, '/home/systemproject1/systemproject1')

from app import app as application  # Required for PythonAnywhere WSGI
from models import db
from config import Config

# Initialize app context, folders, and DB
application.app_context().push()
Config.init_folders()
with application.app_context():
    db.create_all()

