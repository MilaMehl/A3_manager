import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService


def _get_valid_token(app, user_id=1):
    with app.app_context():
        return AuthService()._generate_token(user_id)


def _auth_headers(app, user_id=1):
    return {"Authorization": f"Bearer {_get_valid_token(app, user_id)}"}


VALID_BODY = {
    "latitude": -23.50,
    "longitude": -46.60,
    "request_ids": [1, 2],
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
    "requests_without_coords": [],
}


class TestRouteRoutes:
    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.route_controller.route_service")
    def test_get_route_retorna_200(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.return_value = ROUTE_RESULT
        response = client.post("/api/routes/", json=VALID_BODY, headers=_auth_headers(app))
        assert response.status_code == 200

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.route_controller.route_service")
    def test_get_route_retorna_estrutura_correta(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.return_value = ROUTE_RESULT
        response = client.post("/api/routes/", json=VALID_BODY, headers=_auth_headers(app))
        data = response.get_json()
        assert "total_stops" in data
        assert "total_distance_km" in data
        assert "ordered_stops" in data
        assert "google_maps_url" in data
        assert "origin" in data

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.route_controller.route_service")
    def test_get_route_repassa_parametros_ao_service(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.return_value = ROUTE_RESULT
        client.post("/api/routes/", json=VALID_BODY, headers=_auth_headers(app))
        mock_service.build_route.assert_called_once_with(
            user_lat=-23.50,
            user_lon=-46.60,
            request_ids=[1, 2],
        )

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_sem_latitude_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/routes/",
            json={"longitude": -46.60, "request_ids": [1]},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_sem_longitude_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/routes/",
            json={"latitude": -23.50, "request_ids": [1]},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_request_ids_vazio_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/routes/",
            json={"latitude": -23.50, "longitude": -46.60, "request_ids": []},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_request_ids_nao_lista_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/routes/",
            json={"latitude": -23.50, "longitude": -46.60, "request_ids": "1,2"},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.route_controller.route_service")
    def test_get_route_sem_coordenadas_validas_retorna_400(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.side_effect = ValueError("Nenhum dos requests informados possui coordenadas válidas.")
        response = client.post("/api/routes/", json=VALID_BODY, headers=_auth_headers(app))
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_get_route_sem_token_retorna_401(self, client):
        response = client.post("/api/routes/", json=VALID_BODY)
        assert response.status_code == 401

    def test_get_route_metodo_get_nao_permitido(self, client, app):
        response = client.get("/api/routes/", headers=_auth_headers(app))
        assert response.status_code == 405
