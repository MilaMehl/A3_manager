import pytest
from datetime import datetime
from decimal import Decimal
from app.models.info_grouping_request_model import InfoGroupingRequest


class TestInfoGroupingRequestModel:
    def _make_info(self, **kwargs):
        defaults = dict(
            latitude=Decimal("-23.5505"),
            longitude=Decimal("-46.6333"),
            classification="A",
            status="E",
            created_at=datetime(2024, 6, 15, 10, 0, 0),
            updated_at=datetime(2024, 6, 15, 10, 0, 0),
        )
        defaults.update(kwargs)
        return InfoGroupingRequest(**defaults)

    def test_to_dict_returns_all_fields(self, app):
        with app.app_context():
            info = self._make_info()
            result = info.to_dict()

            assert result["latitude"] == float(Decimal("-23.5505"))
            assert result["longitude"] == float(Decimal("-46.6333"))
            assert result["classification"] == "A"
            assert result["status"] == "E"
            assert "created_at" in result
            assert "updated_at" in result

    def test_to_dict_latitude_longitude_as_float(self, app):
        with app.app_context():
            info = self._make_info(latitude=Decimal("1.1111111"), longitude=Decimal("2.2222222"))
            result = info.to_dict()

            assert isinstance(result["latitude"], float)
            assert isinstance(result["longitude"], float)

    def test_to_dict_no_id_before_persist(self, app):
        with app.app_context():
            info = self._make_info()
            result = info.to_dict()
            assert result.get("id") is None

    def test_persist_and_retrieve(self, app, db):
        with app.app_context():
            info = self._make_info(classification="B", status="F")
            db.session.add(info)
            db.session.commit()

            found = InfoGroupingRequest.query.filter_by(classification="B").first()
            assert found is not None
            assert found.status == "F"
            assert isinstance(float(found.latitude), float)
