from app.configs.database import db
from datetime import datetime


class GroupingRequest(db.Model):
    __tablename__ = "grouping_requests"

    id = db.Column(db.Integer, primary_key=True)
    id_request = db.Column(
        db.Integer,
        db.ForeignKey("requests.id", ondelete="CASCADE"),
        nullable=False,
    )
    id_info_grouping_request = db.Column(
        db.Integer,
        db.ForeignKey("info_grouping_requests.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    request = db.relationship("Request", backref=db.backref("grouping_requests", lazy=True))
    info_grouping_request = db.relationship(
        "InfoGroupingRequest", backref=db.backref("grouping_requests", lazy=True)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "id_request": self.id_request,
            "id_info_grouping_request": self.id_info_grouping_request,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
