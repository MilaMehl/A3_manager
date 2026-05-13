import jwt
import os
from functools import wraps
from flask import request, jsonify
from app.repositories.user_repository import UserRepository

user_repository = UserRepository()


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token de autenticação não fornecido."}), 401

        token = auth_header.split(" ")[1]

        try:
            secret = os.getenv("SECRET_KEY", "dev-secret-key")
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            user = user_repository.find_by_id(int(payload["sub"]))

            if not user:
                return jsonify({"error": "Usuário não encontrado."}), 401

            request.current_user = user

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido."}), 401

        return f(*args, **kwargs)
    return decorated
