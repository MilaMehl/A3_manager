import pytest
from unittest.mock import MagicMock, patch


class TestAuthController:
    @patch("app.controllers.auth_controller.auth_service")
    def test_login_sucesso(self, mock_service, client):
        mock_service.login.return_value = {
            "token": "jwt.token.aqui",
            "user": {"id": 1, "email": "admin@test.com", "nome": "Admin"},
        }
        response = client.post(
            "/api/auth/login",
            json={"email": "admin@test.com", "password": "Admin123!"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "token" in data
        assert data["user"]["email"] == "admin@test.com"

    @patch("app.controllers.auth_controller.auth_service")
    def test_login_credenciais_invalidas_retorna_401(self, mock_service, client):
        mock_service.login.side_effect = ValueError("Email ou senha inválidos.")
        response = client.post(
            "/api/auth/login",
            json={"email": "x@test.com", "password": "errado"},
        )
        assert response.status_code == 401
        assert "error" in response.get_json()

    def test_login_sem_body_retorna_400(self, client):
        response = client.post("/api/auth/login", data="", content_type="application/json")
        assert response.status_code == 400
        data = response.get_json()
        assert data is None or "error" in (data or {})

    def test_login_sem_email_retorna_400(self, client):
        response = client.post("/api/auth/login", json={"password": "Admin123!"})
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_login_sem_password_retorna_400(self, client):
        response = client.post("/api/auth/login", json={"email": "admin@test.com"})
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_login_campos_vazios_retorna_400(self, client):
        response = client.post("/api/auth/login", json={"email": "", "password": ""})
        assert response.status_code == 400
        assert "error" in response.get_json()
