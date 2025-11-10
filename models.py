from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120))
    course_name = db.Column(db.String(120))
    hash = db.Column(db.String(66))
    # ❌ OLD: metadata = db.Column(db.String(256))
    # ✅ NEW:
    metadata_json = db.Column(db.String(256))
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShareLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'))
    link = db.Column(db.String(256))
    expires_at = db.Column(db.DateTime)
