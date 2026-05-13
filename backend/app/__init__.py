from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    # Configuração do banco de dados SQLite
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_db = f"sqlite:///{os.path.join(base_dir, 'instance', 'app.db')}"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", default_db)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)

    # Inicializar extensões
    from app.configs.database import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos para o Alembic detectar
    from app.models import user_model  # noqa: F401
    from app.models import request_model  # noqa: F401
    from app.models import info_grouping_request_model  # noqa: F401
    from app.models import grouping_request_model  # noqa: F401

    # Registrar blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.request_routes import request_bp
    from app.routes.route_routes import route_bp
    from app.routes.grouping_routes import grouping_bp
    from app.routes.grouping_route_routes import grouping_route_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(request_bp, url_prefix="/api/requests")
    app.register_blueprint(route_bp, url_prefix="/api/routes")
    app.register_blueprint(grouping_bp, url_prefix="/api/groupings")
    app.register_blueprint(grouping_route_bp, url_prefix="/api/grouping-routes")

    return app
