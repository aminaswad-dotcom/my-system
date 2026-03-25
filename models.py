from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_number = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sender_receiver = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    notes = db.Column(db.Text)
    doc_type = db.Column(db.String(10), nullable=False)  # 'incoming' or 'outgoing'

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    files = db.relationship('File', backref='document', lazy=True, cascade='all, delete-orphan')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
