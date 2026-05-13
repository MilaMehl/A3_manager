from flask import Blueprint
from app.controllers.route_controller import RouteController
from app.middlewares.auth_middleware import jwt_required

route_bp = Blueprint("routes", __name__)
route_controller = RouteController()


@route_bp.route("/", methods=["POST"])
@jwt_required
def get_route():
    return route_controller.get_route()
