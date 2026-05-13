from flask import Blueprint
from app.controllers.grouping_route_controller import GroupingRouteController
from app.middlewares.auth_middleware import jwt_required

grouping_route_bp = Blueprint("grouping_routes", __name__)
grouping_route_controller = GroupingRouteController()


@grouping_route_bp.route("/", methods=["POST"])
@jwt_required
def get_grouping_route():
    return grouping_route_controller.get_route()
