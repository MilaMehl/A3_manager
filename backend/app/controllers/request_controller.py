from flask import request, jsonify
from app.services.request_service import RequestService

request_service = RequestService()


class RequestController:
    def get_requests(self):
        try:
            date_from = request.args.get("date_from")
            date_to = request.args.get("date_to")
            status = request.args.get("status")
            classification = request.args.get("classification")
            address = request.args.get("address")

            results = request_service.get_filtered(
                date_from=date_from,
                date_to=date_to,
                status=status,
                classification=classification,
                address=address,
            )

            return jsonify({
                "total": len(results),
                "data": results,
            }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
