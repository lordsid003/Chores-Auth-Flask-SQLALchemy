from datetime import datetime
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, description, category, status):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.status = status
