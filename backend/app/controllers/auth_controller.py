from flask import request, jsonify
from app.services.auth_service import AuthService

auth_service = AuthService()


class AuthController:
    def login(self):
        body = request.get_json()

        if not body:
            return jsonify({"error": "Corpo da requisição inválido."}), 400

        email = body.get("email", "").strip()
        password = body.get("password", "").strip()

        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios."}), 400

        try:
            result = auth_service.login(email, password)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
