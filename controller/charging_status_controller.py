from flask import  jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from models.charging_status_entity import ChargingStatusData
from service.charger_status_service import ChargingStatusService

charging_status_controller = Blueprint('charging_status_controller', __name__, url_prefix='/charging/status', description="Informations de charge du controller")

@charging_status_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_charging_status_data():
    service = ChargingStatusService()
    data: ChargingStatusData = service.read_charging_status_data()
    if data is None:
        return jsonify({"error": "Erreur de communication avec la batterie"}), 500

    return jsonify(data.to_dict()), 200