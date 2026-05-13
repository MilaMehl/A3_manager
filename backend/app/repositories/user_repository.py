from app.models.user_model import User


class UserRepository:
    def find_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def find_by_id(self, user_id: int) -> User | None:
        return User.query.get(user_id)
