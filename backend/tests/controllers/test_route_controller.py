import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService


def _get_valid_token(app, user_id=1):
    with app.app_context():
        return AuthService()._generate_token(user_id)


def _auth_headers(app, user_id=1):
    token = _get_valid_token(app, user_id)
    return {"Authorization": f"Bearer {token}"}


VALID_BODY = {
    "latitude": -23.50,
    "longitude": -46.60,
    "request_ids": [1, 2, 3],
}

ROUTE_RESULT = {
    "total_stops": 3,
    "total_distance_km": 5.5,
    "origin": {"latitude": -23.50, "longitude": -46.60},
    "ordered_stops": [],
    "google_maps_url": "https://www.google.com/maps/dir/?api=1&origin=-23.5,-46.6&destination=-23.5,-46.6&travelmode=driving",
    "requests_without_coords": [],
}


class TestRouteController:
    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.route_controller.route_service")
    def test_get_route_sucesso(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.return_value = ROUTE_RESULT
        response = client.post("/api/routes/", json=VALID_BODY, headers=_auth_headers(app))
        assert response.status_code == 200
        data = response.get_json()
        assert data["total_stops"] == 3
        assert "ordered_stops" in data
        assert "google_maps_url" in data

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.route_controller.route_service")
    def test_get_route_repassa_parametros_ao_service(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.return_value = ROUTE_RESULT
        client.post("/api/routes/", json=VALID_BODY, headers=_auth_headers(app))
        mock_service.build_route.assert_called_once_with(
            user_lat=-23.50,
            user_lon=-46.60,
            request_ids=[1, 2, 3],
        )

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_get_route_sem_body_retorna_400(self, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        response = client.post(
            "/api/routes/",
            data="",
            content_type="application/json",
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data is None or "error" in (data or {})

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
            json={"latitude": -23.50, "longitude": -46.60, "request_ids": "1,2,3"},
            headers=_auth_headers(app),
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.route_controller.route_service")
    def test_get_route_service_levanta_valueerror_retorna_400(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.build_route.side_effect = ValueError("Nenhum dos requests informados possui coordenadas válidas.")
        response = client.post("/api/routes/", json=VALID_BODY, headers=_auth_headers(app))
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_get_route_sem_token_retorna_401(self, client):
        response = client.post("/api/routes/", json=VALID_BODY)
        assert response.status_code == 401
