from app.models.request_model import Request
from app.configs.database import db
from datetime import datetime


class RequestRepository:
    def find_by_filters(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        status: str = None,
        classification: str = None,
        address: str = None,
    ) -> list[Request]:
        query = Request.query

        if date_from:
            query = query.filter(Request.date >= date_from)
        if date_to:
            query = query.filter(Request.date <= date_to)
        if status:
            query = query.filter(Request.status.ilike(f"%{status}%"))
        if classification:
            query = query.filter(Request.classification.ilike(f"%{classification}%"))
        if address:
            query = query.filter(Request.address.ilike(f"%{address}%"))

        return query.order_by(Request.date.desc()).all()
