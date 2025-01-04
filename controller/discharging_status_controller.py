from flask import  jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from models.discharging_status_entity import DischargerStatusData
from service.charger_status_service import ChargingStatusService
from service.discharger_status_service import DischargerStatusService

discharging_status_controller = Blueprint('discharging_status_controller', __name__, url_prefix='/discharging/status', description="Informations de décharge du controller")

@discharging_status_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_charging_status_data():
    service = DischargerStatusService()
    data: DischargerStatusData = service.read_discharger_status_data()
    if data is None:
        return jsonify({"error": "Erreur de communication avec la batterie"}), 500

    return data.to_dict, 200