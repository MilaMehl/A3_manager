import math
from app.repositories.route_repository import RouteRepository

route_repository = RouteRepository()


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância em km entre dois pontos geográficos."""
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _nearest_neighbor(origin: tuple, points: list[dict]) -> list[dict]:
    """
    Algoritmo Nearest Neighbor:
    A partir da origem, sempre vai ao ponto mais próximo ainda não visitado.
    Retorna a lista ordenada de pontos.
    """
    remaining = points[:]
    ordered = []
    current = origin

    while remaining:
        nearest = min(
            remaining,
            key=lambda p: _haversine(current[0], current[1], p["latitude"], p["longitude"]),
        )
        distance_from_prev = _haversine(current[0], current[1], nearest["latitude"], nearest["longitude"])
        nearest["distance_from_prev_km"] = round(distance_from_prev, 2)
        ordered.append(nearest)
        current = (nearest["latitude"], nearest["longitude"])
        remaining.remove(nearest)

    return ordered


class RouteService:
    def build_route(self, user_lat: float, user_lon: float, request_ids: list[int]) -> dict:
        # Busca os requests no banco
        requests = route_repository.find_by_ids(request_ids)

        # Filtra apenas os que têm coordenadas
        points = []
        missing_coords = []
        for r in requests:
            if r.latitude is not None and r.longitude is not None:
                points.append({
                    "id": r.id,
                    "address": r.address,
                    "classification": r.classification,
                    "status": r.status,
                    "latitude": float(r.latitude),
                    "longitude": float(r.longitude),
                })
            else:
                missing_coords.append(r.id)

        if not points:
            raise ValueError("Nenhum dos requests informados possui coordenadas válidas.")

        # Ordena pelo algoritmo Nearest Neighbor
        origin = (user_lat, user_lon)
        ordered_points = _nearest_neighbor(origin, points)

        # Calcula distância total
        total_distance_km = sum(p["distance_from_prev_km"] for p in ordered_points)

        # Gera URL do Google Maps
        google_maps_url = self._build_google_maps_url(user_lat, user_lon, ordered_points)

        return {
            "total_stops": len(ordered_points),
            "total_distance_km": round(total_distance_km, 2),
            "origin": {"latitude": user_lat, "longitude": user_lon},
            "ordered_stops": ordered_points,
            "google_maps_url": google_maps_url,
            "requests_without_coords": missing_coords,
        }

    def _build_google_maps_url(
        self, user_lat: float, user_lon: float, ordered_points: list[dict]
    ) -> str:
        """
        Gera URL do Google Maps com origem, waypoints intermediários e destino final.
        Formato:
        https://www.google.com/maps/dir/?api=1
          &origin=lat,lon
          &destination=lat,lon
          &waypoints=lat,lon|lat,lon|...
          &travelmode=driving
        """
        base = "https://www.google.com/maps/dir/?api=1"

        origin = f"{user_lat},{user_lon}"
        destination = f"{ordered_points[-1]['latitude']},{ordered_points[-1]['longitude']}"

        params = f"&origin={origin}&destination={destination}&travelmode=driving"

        # Waypoints são todos os pontos exceto o último (que é o destino)
        if len(ordered_points) > 1:
            waypoints = "|".join(
                f"{p['latitude']},{p['longitude']}" for p in ordered_points[:-1]
            )
            params += f"&waypoints={waypoints}"

        return base + params
