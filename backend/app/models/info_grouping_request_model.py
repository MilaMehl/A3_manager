from app.configs.database import db
from datetime import datetime


class InfoGroupingRequest(db.Model):
    __tablename__ = "info_grouping_requests"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Numeric(10, 7), nullable=False)
    longitude = db.Column(db.Numeric(10, 7), nullable=False)
    classification = db.Column(db.String(1), nullable=False)
    status = db.Column(db.String(1), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "classification": self.classification,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
