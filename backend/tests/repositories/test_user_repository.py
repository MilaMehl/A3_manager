import pytest
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.configs.database import db as _db


def make_user(email="user@test.com", password="hashed_password", nome="Usuário Teste", **kwargs):
    return User(email=email, password=password, nome=nome, **kwargs)


class TestUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self, app, db):
        self.repo = UserRepository()
        self.app = app
        self.db = db

    def test_find_by_email_returns_user(self, app, db):
        with app.app_context():
            db.session.add(make_user(email="joao@test.com"))
            db.session.commit()

            result = self.repo.find_by_email("joao@test.com")
            assert result is not None
            assert result.email == "joao@test.com"

    def test_find_by_email_returns_none_when_not_found(self, app, db):
        with app.app_context():
            result = self.repo.find_by_email("naoexiste@test.com")
            assert result is None

    def test_find_by_email_is_exact_match(self, app, db):
        with app.app_context():
            db.session.add(make_user(email="joao@test.com"))
            db.session.commit()

            result = self.repo.find_by_email("joao@other.com")
            assert result is None

    def test_find_by_id_returns_user(self, app, db):
        with app.app_context():
            u = make_user(email="maria@test.com")
            db.session.add(u)
            db.session.commit()

            result = self.repo.find_by_id(u.id)
            assert result is not None
            assert result.email == "maria@test.com"

    def test_find_by_id_returns_none_when_not_found(self, app, db):
        with app.app_context():
            result = self.repo.find_by_id(9999)
            assert result is None

    def test_find_by_id_returns_correct_user(self, app, db):
        with app.app_context():
            u1 = make_user(email="a@test.com")
            u2 = make_user(email="b@test.com")
            db.session.add_all([u1, u2])
            db.session.commit()

            result = self.repo.find_by_id(u2.id)
            assert result.email == "b@test.com"
