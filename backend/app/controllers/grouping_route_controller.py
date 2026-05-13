from flask import request, jsonify
from app.services.grouping_route_service import GroupingRouteService

grouping_route_service = GroupingRouteService()


class GroupingRouteController:
    def get_route(self):
        body = request.get_json()

        if not body:
            return jsonify({"error": "Corpo da requisição inválido."}), 400

        user_lat = body.get("latitude")
        user_lon = body.get("longitude")
        grouping_ids = body.get("grouping_ids", [])

        if user_lat is None or user_lon is None:
            return jsonify({"error": "Os campos 'latitude' e 'longitude' são obrigatórios."}), 400

        if not isinstance(grouping_ids, list) or len(grouping_ids) == 0:
            return jsonify({"error": "O campo 'grouping_ids' deve ser um array com ao menos um ID."}), 400

        try:
            result = grouping_route_service.build_route(
                user_lat=float(user_lat),
                user_lon=float(user_lon),
                grouping_ids=grouping_ids,
            )
            return jsonify(result), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
