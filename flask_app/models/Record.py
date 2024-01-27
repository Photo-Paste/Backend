from flask_app import db
from datetime import datetime

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Record {self.id} by User {self.user_id}>'
    
    @classmethod
    def create_record(cls, data):
        new_record = cls()
        for key, value in data.items():
            if hasattr(new_record, key):
                setattr(new_record, key, value)
        db.session.add(new_record)
        db.session.commit()
        return new_record
    
    @classmethod
    def delete_record(cls, record_id):
        record = cls.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def update_record(cls, record, updates):
        for key, value in updates.items():
            if hasattr(record, key):
                setattr(record, key, value)
        db.session.commit()