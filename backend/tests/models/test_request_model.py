import pytest
from datetime import datetime
from decimal import Decimal
from app.models.request_model import Request


class TestRequestModel:
    def _make_request(self, **kwargs):
        defaults = dict(
            address="Rua das Flores, 123",
            classification="buraco",
            date=datetime(2024, 6, 15, 10, 0, 0),
            latitude=Decimal("-23.5505"),
            longitude=Decimal("-46.6333"),
            photo_path="photos/test.jpg",
            status="em andamento",
            created_at=datetime(2024, 6, 15, 10, 0, 0),
            updated_at=datetime(2024, 6, 15, 10, 0, 0),
        )
        defaults.update(kwargs)
        return Request(**defaults)

    def test_to_dict_returns_all_fields(self, app):
        with app.app_context():
            r = self._make_request()
            result = r.to_dict()

            assert result["address"] == "Rua das Flores, 123"
            assert result["classification"] == "buraco"
            assert result["date"] == "2024-06-15T10:00:00"
            assert result["latitude"] == float(Decimal("-23.5505"))
            assert result["longitude"] == float(Decimal("-46.6333"))
            assert result["photo_path"] == "photos/test.jpg"
            assert result["status"] == "em andamento"
            assert "created_at" in result
            assert "updated_at" in result

    def test_to_dict_nullable_fields_as_none(self, app):
        with app.app_context():
            r = Request(
                created_at=datetime(2024, 1, 1),
                updated_at=datetime(2024, 1, 1),
            )
            result = r.to_dict()

            assert result["address"] is None
            assert result["classification"] is None
            assert result["date"] is None
            assert result["latitude"] is None
            assert result["longitude"] is None
            assert result["photo_path"] is None
            assert result["status"] is None

    def test_to_dict_latitude_longitude_as_float(self, app):
        with app.app_context():
            r = self._make_request(latitude=Decimal("10.1234567"), longitude=Decimal("-20.7654321"))
            result = r.to_dict()

            assert isinstance(result["latitude"], float)
            assert isinstance(result["longitude"], float)

    def test_persist_and_retrieve(self, app, db):
        with app.app_context():
            r = self._make_request()
            db.session.add(r)
            db.session.commit()

            found = Request.query.filter_by(address="Rua das Flores, 123").first()
            assert found is not None
            assert found.status == "em andamento"
            assert found.classification == "buraco"
