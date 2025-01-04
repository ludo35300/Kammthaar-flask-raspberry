import datetime
from flask import  jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from service.battery_service import BatterieService
from service.bdd_service import BDDService

batterie_controller = Blueprint('batterie_controller', __name__, url_prefix='/batterie', description="Informations de la batterie")

@batterie_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_battery_data():
    service = BatterieService()
    data = service.read_battery_data()
    if data is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500
    
    return jsonify({
        "battery_voltage": data.battery_voltage,
        "battery_amperage": data.battery_amperage,
        "battery_power": data.battery_power,
        "battery_temp": data.battery_temp,
        "battery_pourcent": data.battery_pourcent
    }), 200