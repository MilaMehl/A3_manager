from app.configs.database import db
from datetime import datetime


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(254), nullable=True)
    classification = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    latitude = db.Column(db.Numeric(10, 7), nullable=True)
    longitude = db.Column(db.Numeric(10, 7), nullable=True)
    photo_path = db.Column(db.String(254), nullable=True)
    status = db.Column(db.String(254), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "classification": self.classification,
            "date": self.date.isoformat() if self.date else None,
            "latitude": float(self.latitude) if self.latitude is not None else None,
            "longitude": float(self.longitude) if self.longitude is not None else None,
            "photo_path": self.photo_path,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
