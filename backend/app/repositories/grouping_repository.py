from app.models.info_grouping_request_model import InfoGroupingRequest
from app.models.grouping_request_model import GroupingRequest
from app.models.request_model import Request
from app.configs.database import db


class GroupingRepository:
    def find_all_with_requests(
        self,
        address: str = None,
        status: str = None,
        classification: str = None,
        date_from=None,
        date_to=None,
    ) -> list[InfoGroupingRequest]:
        """
        Retorna todos os InfoGroupingRequests (com filtros opcionais).
        Se address/date_from/date_to forem fornecidos, retorna apenas os grupos
        que possuem ao menos um Request correspondente.
        """
        query = (
            db.session.query(InfoGroupingRequest)
            .join(GroupingRequest, GroupingRequest.id_info_grouping_request == InfoGroupingRequest.id)
            .join(Request, Request.id == GroupingRequest.id_request)
            .distinct()
        )

        if address:
            query = query.filter(Request.address.ilike(f"%{address}%"))
        if status:
            query = query.filter(InfoGroupingRequest.status == status)
        if classification:
            query = query.filter(InfoGroupingRequest.classification == classification)
        if date_from:
            query = query.filter(Request.date >= date_from)
        if date_to:
            query = query.filter(Request.date <= date_to)

        return query.order_by(InfoGroupingRequest.id.asc()).all()


    def find_requests_by_grouping_id(self, grouping_id: int) -> list[Request]:
        """
        Retorna os Requests vinculados a um InfoGroupingRequest específico.
        """
        return (
            db.session.query(Request)
            .join(GroupingRequest, GroupingRequest.id_request == Request.id)
            .filter(GroupingRequest.id_info_grouping_request == grouping_id)
            .order_by(Request.date.asc())
            .all()
        )


    def find_groupings_by_ids(self, grouping_ids: list[int]) -> list[InfoGroupingRequest]:
        """
        Retorna os InfoGroupingRequests pelos IDs fornecidos.
        """
        return (
            db.session.query(InfoGroupingRequest)
            .filter(InfoGroupingRequest.id.in_(grouping_ids))
            .all()
        )
