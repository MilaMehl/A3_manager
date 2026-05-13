import pytest
from unittest.mock import MagicMock, patch
from app.services.grouping_route_service import GroupingRouteService


def _make_info_mock(id=1, lat=-23.55, lon=-46.63, classification="A", status="E"):
    info = MagicMock()
    info.id = id
    info.latitude = lat
    info.longitude = lon
    info.classification = classification
    info.status = status
    return info


ROUTE_RESULT = {
    "total_stops": 2,
    "total_distance_km": 3.5,
    "origin": {"latitude": -23.50, "longitude": -46.60},
    "ordered_stops": [],
    "google_maps_url": "https://www.google.com/maps/dir/?api=1&origin=-23.5,-46.6&destination=-23.55,-46.63&travelmode=driving",
    "groupings_without_coords": [],
}


class TestGroupingRouteService:
    def setup_method(self):
        self.service = GroupingRouteService()

    @patch("app.services.grouping_route_service.grouping_repository")
    def test_build_route_retorna_estrutura_correta(self, mock_repo):
        mock_repo.find_groupings_by_ids.return_value = [
            _make_info_mock(id=1, lat=-23.51, lon=-46.61),
            _make_info_mock(id=2, lat=-23.52, lon=-46.62),
        ]
        result = self.service.build_route(-23.50, -46.60, [1, 2])

        assert result["total_stops"] == 2
        assert result["total_distance_km"] >= 0
        assert "ordered_stops" in result
        assert "google_maps_url" in result
        assert "origin" in result
        assert "groupings_without_coords" in result

    @patch("app.services.grouping_route_service.grouping_repository")
    def test_build_route_sem_coordenadas_levanta_erro(self, mock_repo):
        info = MagicMock()
        info.id = 1
        info.latitude = None
        info.longitude = None
        mock_repo.find_groupings_by_ids.return_value = [info]

        with pytest.raises(ValueError, match="coordenadas válidas"):
            self.service.build_route(-23.50, -46.60, [1])

    @patch("app.services.grouping_route_service.grouping_repository")
    def test_build_route_lista_agrupamentos_sem_coords(self, mock_repo):
        mock_repo.find_groupings_by_ids.return_value = [
            _make_info_mock(id=1, lat=-23.51, lon=-46.61),
            MagicMock(id=2, latitude=None, longitude=None),
        ]
        result = self.service.build_route(-23.50, -46.60, [1, 2])
        assert 2 in result["groupings_without_coords"]

    @patch("app.services.grouping_route_service.grouping_repository")
    def test_build_route_ordena_pelo_mais_proximo(self, mock_repo):
        mock_repo.find_groupings_by_ids.return_value = [
            _make_info_mock(id=1, lat=-23.51, lon=-46.61),   # próximo
            _make_info_mock(id=2, lat=-25.00, lon=-48.00),   # longe
        ]
        result = self.service.build_route(-23.50, -46.60, [1, 2])
        assert result["ordered_stops"][0]["id"] == 1

    @patch("app.services.grouping_route_service.grouping_repository")
    def test_build_route_inclui_distance_from_prev(self, mock_repo):
        mock_repo.find_groupings_by_ids.return_value = [
            _make_info_mock(id=1, lat=-23.51, lon=-46.61),
            _make_info_mock(id=2, lat=-23.52, lon=-46.62),
        ]
        result = self.service.build_route(-23.50, -46.60, [1, 2])
        for stop in result["ordered_stops"]:
            assert "distance_from_prev_km" in stop
            assert stop["distance_from_prev_km"] >= 0

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
