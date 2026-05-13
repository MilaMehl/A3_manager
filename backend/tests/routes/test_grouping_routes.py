import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService


def _get_valid_token(app, user_id=1):
    with app.app_context():
        return AuthService()._generate_token(user_id)


def _auth_headers(app, user_id=1):
    return {"Authorization": f"Bearer {_get_valid_token(app, user_id)}"}


class TestGroupingRoutes:
    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.grouping_controller.grouping_service")
    def test_get_groupings_retorna_200(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_all_groupings.return_value = []
        response = client.get("/api/groupings/", headers=_auth_headers(app))
        assert response.status_code == 200

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.grouping_controller.grouping_service")
    def test_get_groupings_retorna_json_com_total_e_data(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_all_groupings.return_value = [
            {"id": 1, "classification": "A", "status": "E", "total_requests": 2, "requests": []}
        ]
        response = client.get("/api/groupings/", headers=_auth_headers(app))
        data = response.get_json()
        assert "total" in data
        assert "data" in data
        assert data["total"] == 1

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.grouping_controller.grouping_service")
    def test_get_groupings_aceita_todos_os_filtros(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_all_groupings.return_value = []
        response = client.get(
            "/api/groupings/?address=Centro&status=E&classification=A"
            "&date_from=2024-01-01&date_to=2024-12-31",
            headers=_auth_headers(app),
        )
        assert response.status_code == 200
        mock_service.get_all_groupings.assert_called_once_with(
            address="Centro",
            status="E",
            classification="A",
            date_from="2024-01-01",
            date_to="2024-12-31",
        )

    @patch("app.middlewares.auth_middleware.user_repository")
    @patch("app.controllers.grouping_controller.grouping_service")
    def test_get_groupings_erro_interno_retorna_500(self, mock_service, mock_auth, client, app):
        mock_auth.find_by_id.return_value = MagicMock(id=1)
        mock_service.get_all_groupings.side_effect = Exception("Erro inesperado")
        response = client.get("/api/groupings/", headers=_auth_headers(app))
        assert response.status_code == 500
        assert "error" in response.get_json()

    def test_get_groupings_sem_token_retorna_401(self, client):
        response = client.get("/api/groupings/")
        assert response.status_code == 401

    def test_get_groupings_metodo_post_nao_permitido(self, client, app):
        response = client.post("/api/groupings/", headers=_auth_headers(app))
        assert response.status_code == 405
