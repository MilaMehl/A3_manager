from app.models.request_model import Request


class RouteRepository:
    def find_by_ids(self, ids: list[int]) -> list[Request]:
        return Request.query.filter(Request.id.in_(ids)).all()
