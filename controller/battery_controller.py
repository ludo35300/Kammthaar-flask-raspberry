from flask import  jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from models.battery_entity import BatteryData
from service.battery_service import BatterieService

batterie_controller = Blueprint('batterie_controller', __name__, url_prefix='/batterie', description="Informations de la batterie")

@batterie_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_battery_data():
    service = BatterieService()
    data: BatteryData = service.read_battery_data()
    if data is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500
    
    return jsonify(data.to_dict()), 200