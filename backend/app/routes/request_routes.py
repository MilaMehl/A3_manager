from flask import Blueprint
from app.controllers.request_controller import RequestController
from app.middlewares.auth_middleware import jwt_required

request_bp = Blueprint("requests", __name__)
request_controller = RequestController()


@request_bp.route("/", methods=["GET"])
@jwt_required
def get_requests():
    return request_controller.get_requests()
