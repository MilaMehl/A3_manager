import pytest
from datetime import datetime
from decimal import Decimal
from app.models.request_model import Request
from app.models.info_grouping_request_model import InfoGroupingRequest
from app.models.grouping_request_model import GroupingRequest
from app.repositories.grouping_repository import GroupingRepository


def make_request(address="Rua das Flores, 123", classification="buraco",
                 date=None, status="em andamento", **kwargs):
    return Request(
        address=address,
        classification=classification,
        date=date or datetime(2024, 6, 15, 10, 0, 0),
        latitude=Decimal("-23.5505"),
        longitude=Decimal("-46.6333"),
        status=status,
        created_at=datetime(2024, 6, 15),
        updated_at=datetime(2024, 6, 15),
        **kwargs,
    )


def make_info(classification="A", status="E", **kwargs):
    return InfoGroupingRequest(
        latitude=Decimal("-23.5505"),
        longitude=Decimal("-46.6333"),
        classification=classification,
        status=status,
        created_at=datetime(2024, 6, 15),
        updated_at=datetime(2024, 6, 15),
        **kwargs,
    )


def link(db, request, info):
    gr = GroupingRequest(
        id_request=request.id,
        id_info_grouping_request=info.id,
        created_at=datetime(2024, 6, 15),
        updated_at=datetime(2024, 6, 15),
    )
    db.session.add(gr)
    db.session.flush()
    return gr


class TestGroupingRepository:
    @pytest.fixture(autouse=True)
    def setup(self, app, db):
        self.repo = GroupingRepository()
        self.app = app
        self.db = db

    def _seed(self, db, address="Rua das Flores", classification="A",
               status="E", date=None):
        r = make_request(address=address, date=date or datetime(2024, 6, 15))
        info = make_info(classification=classification, status=status)
        db.session.add_all([r, info])
        db.session.flush()
        link(db, r, info)
        db.session.commit()
        return r, info

    def test_find_all_returns_all_groupings(self, app, db):
        with app.app_context():
            self._seed(db, address="Rua A")
            self._seed(db, address="Rua B")

            results = self.repo.find_all_with_requests()
            assert len(results) == 2

    def test_find_all_filter_by_address(self, app, db):
        with app.app_context():
            self._seed(db, address="Rua das Flores")
            self._seed(db, address="Av. Paulista")

            results = self.repo.find_all_with_requests(address="Paulista")
            assert len(results) == 1

    def test_find_all_filter_address_case_insensitive(self, app, db):
        with app.app_context():
            self._seed(db, address="Rua das Flores")

            results = self.repo.find_all_with_requests(address="flores")
            assert len(results) == 1

    def test_find_all_filter_by_status(self, app, db):
        with app.app_context():
            self._seed(db, status="E")
            self._seed(db, status="F")

            results = self.repo.find_all_with_requests(status="E")
            assert len(results) == 1
            assert results[0].status == "E"

    def test_find_all_filter_by_classification(self, app, db):
        with app.app_context():
            self._seed(db, classification="A")
            self._seed(db, classification="B")

            results = self.repo.find_all_with_requests(classification="B")
            assert len(results) == 1
            assert results[0].classification == "B"

    def test_find_all_filter_by_date_from(self, app, db):
        with app.app_context():
            self._seed(db, date=datetime(2024, 1, 1))
            self._seed(db, date=datetime(2024, 8, 1))

            results = self.repo.find_all_with_requests(date_from=datetime(2024, 5, 1))
            assert len(results) == 1

    def test_find_all_filter_by_date_to(self, app, db):
        with app.app_context():
            self._seed(db, date=datetime(2024, 1, 1))
            self._seed(db, date=datetime(2024, 8, 1))

            results = self.repo.find_all_with_requests(date_to=datetime(2024, 5, 1))
            assert len(results) == 1

    def test_find_all_filter_combined(self, app, db):
        with app.app_context():
            self._seed(db, address="Centro", classification="A", status="E")
            self._seed(db, address="Centro", classification="B", status="E")
            self._seed(db, address="Bairro X", classification="A", status="E")

            results = self.repo.find_all_with_requests(address="Centro", classification="A")
            assert len(results) == 1

    def test_find_all_returns_empty_when_no_match(self, app, db):
        with app.app_context():
            self._seed(db, address="Rua das Flores")

            results = self.repo.find_all_with_requests(address="Inexistente")
            assert results == []

    def test_find_requests_by_grouping_id(self, app, db):
        with app.app_context():
            r, info = self._seed(db, address="Rua das Flores")

            requests = self.repo.find_requests_by_grouping_id(info.id)
            assert len(requests) == 1
            assert requests[0].address == "Rua das Flores"

    def test_find_requests_by_grouping_id_multiple_requests(self, app, db):
        with app.app_context():
            r1 = make_request(address="Rua A", date=datetime(2024, 1, 1))
            r2 = make_request(address="Rua B", date=datetime(2024, 3, 1))
            info = make_info()
            db.session.add_all([r1, r2, info])
            db.session.flush()
            link(db, r1, info)
            link(db, r2, info)
            db.session.commit()

            requests = self.repo.find_requests_by_grouping_id(info.id)
            assert len(requests) == 2

    def test_find_requests_by_grouping_id_ordered_by_date(self, app, db):
        with app.app_context():
            r1 = make_request(address="Rua A", date=datetime(2024, 6, 1))
            r2 = make_request(address="Rua B", date=datetime(2024, 1, 1))
            info = make_info()
            db.session.add_all([r1, r2, info])
            db.session.flush()
            link(db, r1, info)
            link(db, r2, info)
            db.session.commit()

            requests = self.repo.find_requests_by_grouping_id(info.id)
            assert requests[0].date < requests[1].date

    def test_find_requests_by_grouping_id_returns_empty_for_unknown(self, app, db):
        with app.app_context():
            results = self.repo.find_requests_by_grouping_id(9999)
            assert results == []
