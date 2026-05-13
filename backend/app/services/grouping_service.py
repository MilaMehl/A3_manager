from datetime import datetime
from flask import request as flask_request
from app.repositories.grouping_repository import GroupingRepository

grouping_repository = GroupingRepository()


class GroupingService:
    def get_all_groupings(
        self,
        address: str = None,
        status: str = None,
        classification: str = None,
        date_from: str = None,
        date_to: str = None,
    ) -> list[dict]:
        parsed_date_from = self._parse_date(date_from)
        parsed_date_to = self._parse_date(date_to)

        groupings = grouping_repository.find_all_with_requests(
            address=address,
            status=status,
            classification=classification,
            date_from=parsed_date_from,
            date_to=parsed_date_to,
        )

        result = []
        for info in groupings:
            requests = grouping_repository.find_requests_by_grouping_id(info.id)
            result.append(self._serialize(info, requests))

        return result

    def _serialize(self, info, requests: list) -> dict:
        return {
            "id": info.id,
            "latitude": float(info.latitude),
            "longitude": float(info.longitude),
            "classification": info.classification,
            "status": info.status,
            "created_at": info.created_at.isoformat(),
            "updated_at": info.updated_at.isoformat(),
            "total_requests": len(requests),
            "requests": [self._serialize_request(r) for r in requests],
        }

    def _serialize_request(self, r) -> dict:
        data = r.to_dict()
        data["photo_url"] = self._build_photo_url(r.photo_path)
        return data

    def _build_photo_url(self, photo_path: str) -> str | None:
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
