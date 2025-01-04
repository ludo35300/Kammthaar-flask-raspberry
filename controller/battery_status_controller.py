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

    return jsonify(data.to_dict()), 200