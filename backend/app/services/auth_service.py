import jwt
import os
from datetime import datetime, timedelta, timezone
from app.repositories.user_repository import UserRepository

user_repository = UserRepository()


class AuthService:
    def login(self, email: str, password: str) -> dict:
        user = user_repository.find_by_email(email)

        if not user or not user.check_password(password):
            raise ValueError("Email ou senha inválidos.")

        token = self._generate_token(user.id)

        return {
            "token": token,
            "user": user.to_dict(),
        }

    def _generate_token(self, user_id: int) -> str:
        secret = os.getenv("SECRET_KEY", "dev-secret-key")
        expires_in = int(os.getenv("JWT_EXPIRATION_HOURS", 24))

        payload = {
            "sub": str(user_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
        }

        return jwt.encode(payload, secret, algorithm="HS256")
