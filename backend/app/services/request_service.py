from datetime import datetime
from flask import request as flask_request
from app.repositories.request_repository import RequestRepository

request_repository = RequestRepository()


class RequestService:
    def get_filtered(
        self,
        date_from: str = None,
        date_to: str = None,
        status: str = None,
        classification: str = None,
        address: str = None,
    ) -> list[dict]:
        parsed_date_from = self._parse_date(date_from)
        parsed_date_to = self._parse_date(date_to)

        requests = request_repository.find_by_filters(
            date_from=parsed_date_from,
            date_to=parsed_date_to,
            status=status,
            classification=classification,
            address=address,
        )

        return [self._serialize(r) for r in requests]

    def _serialize(self, r) -> dict:
        data = r.to_dict()
        data["photo_url"] = self._build_photo_url(r.photo_path)
        return data

    def _build_photo_url(self, photo_path: str) -> str | None:
        """Gera uma URL temporária acessível para a imagem."""
        if not photo_path:
            return None

        base_url = flask_request.host_url.rstrip("/")
        return f"{base_url}/static/{photo_path}"

    def _parse_date(self, value: str) -> datetime | None:
        if not value:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Formato de data inválido: '{value}'. Use YYYY-MM-DD.")
