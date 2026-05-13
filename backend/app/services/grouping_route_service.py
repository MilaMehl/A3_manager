from datetime import datetime
from flask import request as flask_request
from app.repositories.grouping_repository import GroupingRepository
from app.services.route_service import _haversine, _nearest_neighbor

grouping_repository = GroupingRepository()


class GroupingRouteService:
    def build_route(self, user_lat: float, user_lon: float, grouping_ids: list[int]) -> dict:
        groupings = grouping_repository.find_groupings_by_ids(grouping_ids)

        points = []
        missing_coords = []
        for info in groupings:
            if info.latitude is not None and info.longitude is not None:
                points.append({
                    "id": info.id,
                    "latitude": float(info.latitude),
                    "longitude": float(info.longitude),
                    "classification": info.classification,
                    "status": info.status,
                })
            else:
                missing_coords.append(info.id)

        if not points:
            raise ValueError("Nenhum dos agrupamentos informados possui coordenadas válidas.")

        origin = (user_lat, user_lon)
        ordered_points = _nearest_neighbor(origin, points)
        total_distance_km = sum(p["distance_from_prev_km"] for p in ordered_points)
        google_maps_url = self._build_google_maps_url(user_lat, user_lon, ordered_points)

        return {
            "total_stops": len(ordered_points),
            "total_distance_km": round(total_distance_km, 2),
            "origin": {"latitude": user_lat, "longitude": user_lon},
            "ordered_stops": ordered_points,
            "google_maps_url": google_maps_url,
            "groupings_without_coords": missing_coords,
        }

    def _build_google_maps_url(
        self, user_lat: float, user_lon: float, ordered_points: list[dict]
    ) -> str:
        base = "https://www.google.com/maps/dir/?api=1"
        origin = f"{user_lat},{user_lon}"
        destination = f"{ordered_points[-1]['latitude']},{ordered_points[-1]['longitude']}"
        params = f"&origin={origin}&destination={destination}&travelmode=driving"

        if len(ordered_points) > 1:
            waypoints = "|".join(
                f"{p['latitude']},{p['longitude']}" for p in ordered_points[:-1]
            )
            params += f"&waypoints={waypoints}"

        return base + params
