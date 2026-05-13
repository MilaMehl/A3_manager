from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)
auth_controller = AuthController()


@auth_bp.route("/login", methods=["POST"])
def login():
    return auth_controller.login()
