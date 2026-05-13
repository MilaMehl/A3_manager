import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService


def _get_valid_token(app, user_id=1):
    with app.app_context():
        return AuthService()._generate_token(user_id)


def _auth_headers(app, user_id=1):
    token = _get_valid_token(app, user_id)
    return {"Authorization": f"Bearer {token}"}


class TestRequestController:
    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.request_controller.request_service")
    def test_get_requests_retorna_lista(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_filtered.return_value = [
            {"id": 1, "address": "Rua A", "status": "em andamento", "photo_url": None}
        ]
        response = client.get("/api/requests/", headers=_auth_headers(app))
        assert response.status_code == 200
        data = response.get_json()
        assert data["total"] == 1
        assert len(data["data"]) == 1

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.request_controller.request_service")
    def test_get_requests_lista_vazia(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_filtered.return_value = []
        response = client.get("/api/requests/", headers=_auth_headers(app))
        assert response.status_code == 200
        data = response.get_json()
        assert data["total"] == 0
        assert data["data"] == []

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.request_controller.request_service")
    def test_get_requests_repassa_filtros(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_filtered.return_value = []
        client.get(
            "/api/requests/?status=em+andamento&classification=buraco&address=Paulista"
            "&date_from=2024-01-01&date_to=2024-12-31",
            headers=_auth_headers(app),
        )
        mock_service.get_filtered.assert_called_once_with(
            date_from="2024-01-01",
            date_to="2024-12-31",
            status="em andamento",
            classification="buraco",
            address="Paulista",
        )

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.request_controller.request_service")
    def test_get_requests_data_invalida_retorna_400(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_filtered.side_effect = ValueError("Formato de data inválido: '01-01-2024'.")
        response = client.get("/api/requests/?date_from=01-01-2024", headers=_auth_headers(app))
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_get_requests_sem_token_retorna_401(self, client):
        response = client.get("/api/requests/")
        assert response.status_code == 401
