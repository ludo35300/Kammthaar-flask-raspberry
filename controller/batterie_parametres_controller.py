from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from models.battery_parametres_entity import BatteryParametresData
from service.batterie_parametres_service import BatterieParametresService

batterie_parametres_controller = Blueprint('batterie_parametres_controller', __name__, url_prefix='/batterie', description="Paramètres de la batterie")



@batterie_parametres_controller.route('/parametres/realtime', methods=['GET'])
@jwt_required()
def get_battery_parametres_data():
    service = BatterieParametresService()
    parametres_battery: BatteryParametresData = service.read_battery_parametres_data()

    if parametres_battery is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify(parametres_battery.to_dict()), 200
