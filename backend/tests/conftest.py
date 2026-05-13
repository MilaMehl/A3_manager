import pytest
import os
from app import create_app
from app.configs.database import db as _db


@pytest.fixture(scope="session")
def app():
    """Cria a aplicação Flask configurada para testes."""
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["JWT_EXPIRATION_HOURS"] = "1"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    """Garante que o banco está limpo a cada teste."""
    with app.app_context():
        yield _db
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture(scope="function")
def client(app):
    """Cliente HTTP para testes de integração."""
    return app.test_client()


@pytest.fixture(scope="function")
def app_context(app):
    """Contexto de aplicação ativo."""
    with app.app_context():
        yield
