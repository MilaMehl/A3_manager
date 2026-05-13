import pytest
from datetime import datetime
from decimal import Decimal
from app.models.request_model import Request
from app.repositories.route_repository import RouteRepository


def make_request(db, **kwargs):
    defaults = dict(
        address="Rua das Flores, 123",
        classification="buraco",
        date=datetime(2024, 6, 15, 10, 0, 0),
        latitude=Decimal("-23.5505"),
        longitude=Decimal("-46.6333"),
        status="em andamento",
        created_at=datetime(2024, 6, 15),
        updated_at=datetime(2024, 6, 15),
    )
    defaults.update(kwargs)
    r = Request(**defaults)
    db.session.add(r)
    db.session.flush()
    return r


class TestRouteRepository:
    @pytest.fixture(autouse=True)
    def setup(self, app, db):
        self.repo = RouteRepository()
        self.app = app
        self.db = db

    def test_find_by_ids_returns_matching_requests(self, app, db):
        with app.app_context():
            r1 = make_request(db, address="Rua A")
            r2 = make_request(db, address="Rua B")
            r3 = make_request(db, address="Rua C")
            db.session.commit()

            results = self.repo.find_by_ids([r1.id, r3.id])
            ids = [r.id for r in results]
            assert r1.id in ids
            assert r3.id in ids
            assert r2.id not in ids

    def test_find_by_ids_returns_all_when_all_ids_given(self, app, db):
        with app.app_context():
            r1 = make_request(db)
            r2 = make_request(db)
            db.session.commit()

            results = self.repo.find_by_ids([r1.id, r2.id])
            assert len(results) == 2

    def test_find_by_ids_returns_empty_for_unknown_ids(self, app, db):
        with app.app_context():
            results = self.repo.find_by_ids([9999, 8888])
            assert results == []

    def test_find_by_ids_returns_empty_for_empty_list(self, app, db):
        with app.app_context():
            results = self.repo.find_by_ids([])
            assert results == []

    def test_find_by_ids_returns_correct_data(self, app, db):
        with app.app_context():
            r = make_request(db, address="Av. Paulista, 1000", classification="iluminacao")
            db.session.commit()

            results = self.repo.find_by_ids([r.id])
            assert len(results) == 1
            assert results[0].address == "Av. Paulista, 1000"
            assert results[0].classification == "iluminacao"
