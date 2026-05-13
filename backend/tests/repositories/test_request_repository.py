import pytest
from datetime import datetime
from decimal import Decimal
from app.models.request_model import Request
from app.repositories.request_repository import RequestRepository


def make_request(**kwargs):
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


class TestRequestRepository:
    @pytest.fixture(autouse=True)
    def setup(self, app, db):
        self.repo = RequestRepository()
        self.app = app
        self.db = db

    def test_find_by_filters_returns_all_when_no_filters(self, app, db):
        with app.app_context():
            db.session.add(make_request(address="Rua A"))
            db.session.add(make_request(address="Rua B"))
            db.session.commit()

            results = self.repo.find_by_filters()
            assert len(results) == 2

    def test_find_by_filters_by_status(self, app, db):
        with app.app_context():
            db.session.add(make_request(status="em andamento"))
            db.session.add(make_request(status="concluido"))
            db.session.commit()

            results = self.repo.find_by_filters(status="concluido")
            assert len(results) == 1
            assert results[0].status == "concluido"

    def test_find_by_filters_by_classification(self, app, db):
        with app.app_context():
            db.session.add(make_request(classification="buraco"))
            db.session.add(make_request(classification="iluminacao"))
            db.session.commit()

            results = self.repo.find_by_filters(classification="iluminacao")
            assert len(results) == 1
            assert results[0].classification == "iluminacao"

    def test_find_by_filters_by_address(self, app, db):
        with app.app_context():
            db.session.add(make_request(address="Rua das Flores, 10"))
            db.session.add(make_request(address="Av. Paulista, 100"))
            db.session.commit()

            results = self.repo.find_by_filters(address="Paulista")
            assert len(results) == 1
            assert "Paulista" in results[0].address

    def test_find_by_filters_address_case_insensitive(self, app, db):
        with app.app_context():
            db.session.add(make_request(address="Rua das Flores, 10"))
            db.session.commit()

            results = self.repo.find_by_filters(address="flores")
            assert len(results) == 1

    def test_find_by_filters_by_date_from(self, app, db):
        with app.app_context():
            db.session.add(make_request(date=datetime(2024, 1, 1)))
            db.session.add(make_request(date=datetime(2024, 6, 1)))
            db.session.commit()

            results = self.repo.find_by_filters(date_from=datetime(2024, 3, 1))
            assert len(results) == 1
            assert results[0].date == datetime(2024, 6, 1)

    def test_find_by_filters_by_date_to(self, app, db):
        with app.app_context():
            db.session.add(make_request(date=datetime(2024, 1, 1)))
            db.session.add(make_request(date=datetime(2024, 6, 1)))
            db.session.commit()

            results = self.repo.find_by_filters(date_to=datetime(2024, 3, 1))
            assert len(results) == 1
            assert results[0].date == datetime(2024, 1, 1)

    def test_find_by_filters_date_range(self, app, db):
        with app.app_context():
            db.session.add(make_request(date=datetime(2024, 1, 1)))
            db.session.add(make_request(date=datetime(2024, 5, 1)))
            db.session.add(make_request(date=datetime(2024, 12, 1)))
            db.session.commit()

            results = self.repo.find_by_filters(
                date_from=datetime(2024, 3, 1),
                date_to=datetime(2024, 8, 1),
            )
            assert len(results) == 1
            assert results[0].date == datetime(2024, 5, 1)

    def test_find_by_filters_combined(self, app, db):
        with app.app_context():
            db.session.add(make_request(status="em andamento", classification="buraco", address="Centro"))
            db.session.add(make_request(status="concluido", classification="buraco", address="Centro"))
            db.session.add(make_request(status="em andamento", classification="iluminacao", address="Centro"))
            db.session.commit()

            results = self.repo.find_by_filters(status="em andamento", classification="buraco")
            assert len(results) == 1
            assert results[0].status == "em andamento"
            assert results[0].classification == "buraco"

    def test_find_by_filters_returns_empty_when_no_match(self, app, db):
        with app.app_context():
            db.session.add(make_request(status="em andamento"))
            db.session.commit()

            results = self.repo.find_by_filters(status="inexistente")
            assert results == []

    def test_find_by_filters_ordered_by_date_desc(self, app, db):
        with app.app_context():
            db.session.add(make_request(date=datetime(2024, 1, 1)))
            db.session.add(make_request(date=datetime(2024, 6, 1)))
            db.session.add(make_request(date=datetime(2024, 3, 1)))
            db.session.commit()

            results = self.repo.find_by_filters()
            dates = [r.date for r in results]
            assert dates == sorted(dates, reverse=True)
