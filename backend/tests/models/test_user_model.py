import pytest
from app.models.user_model import User
from app.configs.database import db


class TestUserModel:
    def test_set_password_hashes_password(self, app):
        with app.app_context():
            user = User(nome="Teste", email="teste@teste.com")
            user.set_password("Senha123!")
            assert user.password != "Senha123!"
            assert user.password is not None

    def test_check_password_correct(self, app):
        with app.app_context():
            user = User(nome="Teste", email="teste@teste.com")
            user.set_password("Senha123!")
            assert user.check_password("Senha123!") is True

    def test_check_password_incorrect(self, app):
        with app.app_context():
            user = User(nome="Teste", email="teste@teste.com")
            user.set_password("Senha123!")
            assert user.check_password("SenhaErrada") is False

    def test_to_dict_returns_expected_fields(self, app):
        with app.app_context():
            from datetime import datetime
            user = User(
                nome="Admin",
                email="admin@sistema.com.br",
                created_at=datetime(2024, 1, 1, 12, 0, 0),
                updated_at=datetime(2024, 1, 1, 12, 0, 0),
            )
            user.set_password("Admin123!")
            result = user.to_dict()

            assert result["nome"] == "Admin"
            assert result["email"] == "admin@sistema.com.br"
            assert "password" not in result
            assert "created_at" in result
            assert "updated_at" in result
