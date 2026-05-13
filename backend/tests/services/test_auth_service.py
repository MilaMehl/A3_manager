import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService


class TestAuthService:
    def setup_method(self):
        self.service = AuthService()

    def _make_user(self, id=1, email="admin@sistema.com.br", nome="Admin"):
        user = MagicMock()
        user.id = id
        user.email = email
        user.nome = nome
        user.check_password = MagicMock(return_value=True)
        user.to_dict = MagicMock(return_value={"id": id, "email": email, "nome": nome})
        return user

    @patch("app.services.auth_service.user_repository")
    def test_login_retorna_token_e_usuario(self, mock_repo):
        user = self._make_user()
        mock_repo.find_by_email.return_value = user

        result = self.service.login("admin@sistema.com.br", "Admin123!")

        assert "token" in result
        assert "user" in result
        assert result["user"]["email"] == "admin@sistema.com.br"

    @patch("app.services.auth_service.user_repository")
    def test_login_usuario_nao_encontrado(self, mock_repo):
        mock_repo.find_by_email.return_value = None

        with pytest.raises(ValueError, match="Email ou senha inválidos"):
            self.service.login("naoexiste@teste.com", "qualquersenha")

    @patch("app.services.auth_service.user_repository")
    def test_login_senha_incorreta(self, mock_repo):
        user = self._make_user()
        user.check_password.return_value = False
        mock_repo.find_by_email.return_value = user

        with pytest.raises(ValueError, match="Email ou senha inválidos"):
            self.service.login("admin@sistema.com.br", "SenhaErrada!")

    def test_generate_token_retorna_string(self, app):
        with app.app_context():
            token = self.service._generate_token(1)
            assert isinstance(token, str)
            assert len(token) > 0

    def test_generate_token_decodificavel(self, app):
        import jwt, os
        with app.app_context():
            token = self.service._generate_token(42)
            secret = os.getenv("SECRET_KEY", "dev-secret-key")
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            assert payload["sub"] == "42"
