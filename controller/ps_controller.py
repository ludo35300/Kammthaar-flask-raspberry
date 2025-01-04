from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from service.ps_service import PSService

ps_controller = Blueprint('ps_controller', __name__, url_prefix='/ps', description="")

@ps_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_ps_data():
    service = PSService()
    data_ps = service.read_ps_data()
    if data_ps is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify({
        "ps_voltage": data_ps.ps_voltage,
        "ps_amperage": data_ps.ps_amperage,
        "ps_power": data_ps.ps_power
    }), 200