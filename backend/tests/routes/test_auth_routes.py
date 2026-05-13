import pytest
import jwt
import os
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService


def _get_valid_token(user_id=1):
    service = AuthService()
    return service._generate_token(user_id)


class TestAuthMiddleware:
    def test_sem_token_retorna_401(self, client):
        response = client.get("/api/requests/")
        assert response.status_code == 401

    def test_token_invalido_retorna_401(self, client):
        response = client.get(
            "/api/requests/",
            headers={"Authorization": "Bearer token.invalido.aqui"}
        )
        assert response.status_code == 401

    def test_token_sem_bearer_retorna_401(self, client):
        response = client.get(
            "/api/requests/",
            headers={"Authorization": "token-sem-bearer"}
        )
        assert response.status_code == 401

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_token_valido_permite_acesso(self, mock_repo, client, app):
        with app.app_context():
            user = MagicMock()
            user.id = 1
            user.email = "admin@sistema.com.br"
            mock_repo.find_by_id.return_value = user

            token = _get_valid_token(1)

        response = client.get(
            "/api/requests/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

    @patch("app.middlewares.auth_middleware.user_repository")
    def test_token_usuario_nao_encontrado_retorna_401(self, mock_repo, client, app):
        with app.app_context():
            mock_repo.find_by_id.return_value = None
            token = _get_valid_token(999)
            response = client.get(
                "/api/requests/",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 401

    def test_token_expirado_retorna_401(self, client, app):
        from datetime import datetime, timedelta, timezone
        with app.app_context():
            secret = os.getenv("SECRET_KEY", "dev-secret-key")
            payload = {
                "sub": 1,
                "iat": datetime.now(timezone.utc) - timedelta(hours=2),
                "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            }
            expired_token = jwt.encode(payload, secret, algorithm="HS256")
            response = client.get(
                "/api/requests/",
                headers={"Authorization": f"Bearer {expired_token}"}
            )
            assert response.status_code == 401


class TestAuthRoute:
    def test_login_sucesso(self, client, app, db):
        with app.app_context():
            from app.models.user_model import User
            from app.configs.database import db as _db
            user = User(nome="Admin", email="admin@test.com")
            user.set_password("Admin123!")
            _db.session.add(user)
            _db.session.commit()

        response = client.post(
            "/api/auth/login",
            json={"email": "admin@test.com", "password": "Admin123!"}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "token" in data
        assert "user" in data

    def test_login_senha_errada(self, client, app, db):
        with app.app_context():
            from app.models.user_model import User
            from app.configs.database import db as _db
            user = User(nome="Admin", email="admin2@test.com")
            user.set_password("Admin123!")
            _db.session.add(user)
            _db.session.commit()

        response = client.post(
            "/api/auth/login",
            json={"email": "admin2@test.com", "password": "SenhaErrada"}
        )
        assert response.status_code == 401

    def test_login_email_nao_cadastrado(self, client):
        response = client.post(
            "/api/auth/login",
            json={"email": "naoexiste@teste.com", "password": "qualquer"}
        )
        assert response.status_code == 401

    def test_login_sem_body_retorna_erro(self, client):
        response = client.post("/api/auth/login", json={})
        assert response.status_code in (400, 401)
