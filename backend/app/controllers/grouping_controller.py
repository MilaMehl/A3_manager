from flask import jsonify, request
from app.services.grouping_service import GroupingService

grouping_service = GroupingService()


class GroupingController:
    def get_groupings(self):
        try:
            address = request.args.get("address")
            status = request.args.get("status")
            classification = request.args.get("classification")
            date_from = request.args.get("date_from")
            date_to = request.args.get("date_to")

            results = grouping_service.get_all_groupings(
                address=address,
                status=status,
                classification=classification,
                date_from=date_from,
                date_to=date_to,
            )
            return jsonify({
                "total": len(results),
                "data": results,
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
