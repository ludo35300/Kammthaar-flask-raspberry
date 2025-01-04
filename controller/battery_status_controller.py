from flask import  jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from service.battery_service import BatterieService

batterie_status_controller = Blueprint('batterie_status_controller', __name__, url_prefix='/batterie/status', description="Informations des erreurs de la batterie")

@batterie_status_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_battery_data():
    service = BatterieService()
    data = service.read_battery_status_data()
    if data is None:
        return jsonify({"error": "Erreur de communication avec la batterie"}), 500

    return jsonify({
        "wrong_identifaction_for_rated_voltage": data.wrong_identifaction_for_rated_voltage,
        "battery_inner_resistence_abnormal": data.battery_inner_resistence_abnormal,
        "temperature_warning_status": data.temperature_warning_status,
        "battery_status": data.battery_status
    }), 200