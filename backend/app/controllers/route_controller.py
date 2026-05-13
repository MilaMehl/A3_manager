from flask import request, jsonify
from app.services.route_service import RouteService

route_service = RouteService()


class RouteController:
    def get_route(self):
        body = request.get_json()

        if not body:
            return jsonify({"error": "Corpo da requisição inválido."}), 400

        user_lat = body.get("latitude")
        user_lon = body.get("longitude")
        request_ids = body.get("request_ids", [])

        if user_lat is None or user_lon is None:
            return jsonify({"error": "Os campos 'latitude' e 'longitude' são obrigatórios."}), 400

        if not isinstance(request_ids, list) or len(request_ids) == 0:
            return jsonify({"error": "O campo 'request_ids' deve ser um array com ao menos um ID."}), 400

        try:
            result = route_service.build_route(
                user_lat=float(user_lat),
                user_lon=float(user_lon),
                request_ids=request_ids,
            )
            return jsonify(result), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
