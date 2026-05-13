import pytest
from datetime import datetime
from decimal import Decimal
from app.models.request_model import Request
from app.models.info_grouping_request_model import InfoGroupingRequest
from app.models.grouping_request_model import GroupingRequest
from app.configs.database import db as _db


class TestGroupingRequestModel:
    def _create_request(self, db):
        r = Request(
            address="Av. Paulista, 1000",
            classification="iluminacao",
            date=datetime(2024, 7, 1, 8, 0, 0),
            latitude=Decimal("-23.5600"),
            longitude=Decimal("-46.6500"),
            status="em andamento",
            created_at=datetime(2024, 7, 1),
            updated_at=datetime(2024, 7, 1),
        )
        db.session.add(r)
        db.session.flush()
        return r

    def _create_info(self, db):
        info = InfoGroupingRequest(
            latitude=Decimal("-23.5600"),
            longitude=Decimal("-46.6500"),
            classification="A",
            status="E",
            created_at=datetime(2024, 7, 1),
            updated_at=datetime(2024, 7, 1),
        )
        db.session.add(info)
        db.session.flush()
        return info

    def test_to_dict_returns_all_fields(self, app, db):
        with app.app_context():
            r = self._create_request(db)
            info = self._create_info(db)

            gr = GroupingRequest(
                id_request=r.id,
                id_info_grouping_request=info.id,
                created_at=datetime(2024, 7, 1),
                updated_at=datetime(2024, 7, 1),
            )
            db.session.add(gr)
            db.session.commit()

            result = gr.to_dict()
            assert result["id_request"] == r.id
            assert result["id_info_grouping_request"] == info.id
            assert "created_at" in result
            assert "updated_at" in result

    def test_relationship_request(self, app, db):
        with app.app_context():
            r = self._create_request(db)
            info = self._create_info(db)

            gr = GroupingRequest(
                id_request=r.id,
                id_info_grouping_request=info.id,
                created_at=datetime(2024, 7, 1),
                updated_at=datetime(2024, 7, 1),
            )
            db.session.add(gr)
            db.session.commit()

            assert gr.request.address == "Av. Paulista, 1000"
            assert gr.request.classification == "iluminacao"

    def test_relationship_info_grouping(self, app, db):
        with app.app_context():
            r = self._create_request(db)
            info = self._create_info(db)

            gr = GroupingRequest(
                id_request=r.id,
                id_info_grouping_request=info.id,
                created_at=datetime(2024, 7, 1),
                updated_at=datetime(2024, 7, 1),
            )
            db.session.add(gr)
            db.session.commit()

            assert gr.info_grouping_request.classification == "A"
            assert gr.info_grouping_request.status == "E"

    def test_cascade_delete_request(self, app, db):
        with app.app_context():
            db.session.execute(_db.text("PRAGMA foreign_keys = ON"))

            r = self._create_request(db)
            info = self._create_info(db)

            gr = GroupingRequest(
                id_request=r.id,
                id_info_grouping_request=info.id,
                created_at=datetime(2024, 7, 1),
                updated_at=datetime(2024, 7, 1),
            )
            db.session.add(gr)
            db.session.commit()
            gr_id = gr.id

            db.session.execute(_db.delete(Request).where(Request.id == r.id))
            db.session.commit()

            assert GroupingRequest.query.filter_by(id=gr_id).first() is None

    def test_persist_multiple_groupings(self, app, db):
        with app.app_context():
            r1 = self._create_request(db)
            r2 = self._create_request(db)
            info = self._create_info(db)

            gr1 = GroupingRequest(id_request=r1.id, id_info_grouping_request=info.id,
                                  created_at=datetime(2024, 7, 1), updated_at=datetime(2024, 7, 1))
            gr2 = GroupingRequest(id_request=r2.id, id_info_grouping_request=info.id,
                                  created_at=datetime(2024, 7, 1), updated_at=datetime(2024, 7, 1))
            db.session.add_all([gr1, gr2])
            db.session.commit()

            count = GroupingRequest.query.filter_by(id_info_grouping_request=info.id).count()
            assert count == 2
