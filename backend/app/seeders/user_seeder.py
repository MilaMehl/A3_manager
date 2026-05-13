from app.configs.database import db
from app.models.user_model import User


def seed_admin():
    """Cria o usuário admin padrão se ainda não existir."""
    existing = User.query.filter_by(email="admin@sistema.com.br").first()
    if existing:
        print("[seeder] Usuário admin já existe, pulando...")
        return

    admin = User(nome="Administrador", email="admin@sistema.com.br")
    admin.set_password("Admin123!")
    db.session.add(admin)
    db.session.commit()
    print("[seeder] Usuário admin criado com sucesso.")
