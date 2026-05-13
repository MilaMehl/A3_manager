import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService


def _auth_headers(app, user_id=1):
    with app.app_context():
        token = AuthService()._generate_token(user_id)
    return {"Authorization": f"Bearer {token}"}


VALID_BODY = {
    "latitude": -23.50,
    "longitude": -46.60,
    "grouping_ids": [1, 2],
}

ROUTE_RESULT = {
    "total_stops": 2,
    "total_distance_km": 3.5,
    "origin": {"latitude": -23.50, "longitude": -46.60},
    "ordered_stops": [
        {"id": 1, "latitude": -23.51, "longitude": -46.61, "distance_from_prev_km": 1.5},
        {"id": 2, "latitude": -23.52, "longitude": -46.62, "distance_from_prev_km": 2.0},
    ],
    "google_maps_url": "https://www.google.com/maps/dir/?api=1&origin=-23.5,-46.6&destination=-23.52,-46.62&travelmode=driving",
    "groupings_without_coords": [],
}


class TestGroupingRouteController:
    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.grouping_route_controller.grouping_route_service")
    def test_get_route_sucesso(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.return_value = ROUTE_RESULT
        response = client.post("/api/grouping-routes/", json=VALID_BODY, headers=_auth_headers(app))
        assert response.status_code == 200
        data = response.get_json()
        assert data["total_stops"] == 2
        assert "ordered_stops" in data
        assert "google_maps_url" in data

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.grouping_route_controller.grouping_route_service")
    def test_get_route_repassa_parametros_ao_service(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.return_value = ROUTE_RESULT
        client.post("/api/grouping-routes/", json=VALID_BODY, headers=_auth_headers(app))
        mock_service.build_route.assert_called_once_with(
            user_lat=-23.50,
            user_lon=-46.60,
            grouping_ids=[1, 2],
        )

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_sem_body_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/grouping-routes/",
            data="",
            content_type="application/json",
            headers=_auth_headers(app),
        )
        assert response.status_code == 400

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_sem_latitude_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/grouping-routes/",
            json={"longitude": -46.60, "grouping_ids": [1]},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_sem_longitude_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/grouping-routes/",
            json={"latitude": -23.50, "grouping_ids": [1]},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_grouping_ids_vazio_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/grouping-routes/",
            json={"latitude": -23.50, "longitude": -46.60, "grouping_ids": []},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_grouping_ids_nao_lista_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/grouping-routes/",
            json={"latitude": -23.50, "longitude": -46.60, "grouping_ids": "1,2"},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.grouping_route_controller.grouping_route_service")
    def test_get_route_sem_coordenadas_validas_retorna_400(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.side_effect = ValueError("Nenhum dos agrupamentos informados possui coordenadas válidas.")
        response = client.post("/api/grouping-routes/", json=VALID_BODY, headers=_auth_headers(app))
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_get_route_sem_token_retorna_401(self, client):
        response = client.post("/api/grouping-routes/", json=VALID_BODY)
        assert response.status_code == 401
