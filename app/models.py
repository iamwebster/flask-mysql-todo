from app.database import db
from datetime import datetime 


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
