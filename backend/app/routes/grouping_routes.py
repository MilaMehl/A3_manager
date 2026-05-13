from flask import Blueprint
from app.controllers.grouping_controller import GroupingController
from app.middlewares.auth_middleware import jwt_required

grouping_bp = Blueprint("groupings", __name__)
grouping_controller = GroupingController()


@grouping_bp.route("/", methods=["GET"])
@jwt_required
def get_groupings():
    return grouping_controller.get_groupings()
