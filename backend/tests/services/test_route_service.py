import pytest
from unittest.mock import MagicMock, patch
from app.services.route_service import RouteService, _haversine, _nearest_neighbor


class TestHaversine:
    def test_mesma_posicao_distancia_zero(self):
        dist = _haversine(-23.5, -46.6, -23.5, -46.6)
        assert dist == pytest.approx(0.0, abs=1e-6)

    def test_distancia_conhecida_sp_rj(self):
        # São Paulo → Rio de Janeiro ≈ 357 km em linha reta
        dist = _haversine(-23.5505, -46.6333, -22.9068, -43.1729)
        assert 340 < dist < 380

    def test_distancia_positiva(self):
        dist = _haversine(-23.0, -46.0, -24.0, -47.0)
        assert dist > 0


class TestNearestNeighbor:
    def _make_point(self, id, lat, lon):
        return {"id": id, "latitude": lat, "longitude": lon, "address": f"Ponto {id}"}

    def test_retorna_todos_os_pontos(self):
        origin = (-23.5, -46.6)
        points = [
            self._make_point(1, -23.51, -46.61),
            self._make_point(2, -23.52, -46.62),
            self._make_point(3, -23.53, -46.63),
        ]
        result = _nearest_neighbor(origin, points)
        assert len(result) == 3

    def test_primeiro_ponto_e_o_mais_proximo(self):
        origin = (-23.5, -46.6)
        points = [
            self._make_point(1, -23.51, -46.61),   # mais próximo
            self._make_point(2, -25.0, -48.0),     # mais longe
        ]
        result = _nearest_neighbor(origin, points)
        assert result[0]["id"] == 1

    def test_cada_ponto_tem_distance_from_prev(self):
        origin = (-23.5, -46.6)
        points = [
            self._make_point(1, -23.51, -46.61),
            self._make_point(2, -23.52, -46.62),
        ]
        result = _nearest_neighbor(origin, points)
        for p in result:
            assert "distance_from_prev_km" in p
            assert p["distance_from_prev_km"] >= 0

    def test_ponto_unico(self):
        origin = (-23.5, -46.6)
        points = [self._make_point(1, -23.51, -46.61)]
        result = _nearest_neighbor(origin, points)
        assert len(result) == 1


class TestRouteService:
    def setup_method(self):
        self.service = RouteService()

    def _make_request_mock(self, id, lat, lon):
        r = MagicMock()
        r.id = id
        r.latitude = lat
        r.longitude = lon
        r.address = f"Rua {id}"
        r.classification = "A"
        r.status = "pending"
        return r

    @patch("app.services.route_service.route_repository")
    def test_build_route_retorna_estrutura_correta(self, mock_repo):
        mock_repo.find_by_ids.return_value = [
            self._make_request_mock(1, -23.51, -46.61),
            self._make_request_mock(2, -23.52, -46.62),
        ]
        result = self.service.build_route(-23.50, -46.60, [1, 2])

        assert result["total_stops"] == 2
        assert result["total_distance_km"] >= 0
        assert "ordered_stops" in result
        assert "google_maps_url" in result
        assert "origin" in result

    @patch("app.services.route_service.route_repository")
    def test_build_route_sem_coordenadas_levanta_erro(self, mock_repo):
        r = MagicMock()
        r.id = 1
        r.latitude = None
        r.longitude = None
        mock_repo.find_by_ids.return_value = [r]

        with pytest.raises(ValueError, match="coordenadas válidas"):
            self.service.build_route(-23.50, -46.60, [1])

    @patch("app.services.route_service.route_repository")
    def test_build_route_requests_sem_coords_listados(self, mock_repo):
        mock_repo.find_by_ids.return_value = [
            self._make_request_mock(1, -23.51, -46.61),
            MagicMock(id=2, latitude=None, longitude=None),
        ]
        result = self.service.build_route(-23.50, -46.60, [1, 2])
        assert 2 in result["requests_without_coords"]

    def test_build_google_maps_url_unico_ponto(self):
        points = [{"latitude": -23.51, "longitude": -46.61}]
        url = self.service._build_google_maps_url(-23.50, -46.60, points)
        assert "google.com/maps" in url
        assert "origin=-23.5,-46.6" in url
        assert "destination=-23.51,-46.61" in url
        assert "waypoints" not in url

    def test_build_google_maps_url_multiplos_pontos(self):
        points = [
            {"latitude": -23.51, "longitude": -46.61},
            {"latitude": -23.52, "longitude": -46.62},
        ]
        url = self.service._build_google_maps_url(-23.50, -46.60, points)
        assert "waypoints" in url
        assert "destination=-23.52,-46.62" in url
