from flask_app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    records = db.relationship('Record', backref='user', lazy=True, cascade="all, delete-orphan")
    email = db.Column(db.String(120), unique=True, nullable=True)
    profile_image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
    @classmethod
    def create_user(cls, data):
        new_user = cls()
        for key, value in data.items():
            if hasattr(new_user, key):
                setattr(new_user, key, value)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def delete_user(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @classmethod
    def update_user(cls, user, updates):
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
