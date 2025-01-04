from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from models.controller_entity import ControllerData
from service.mppt_service import MPPTService

mppt_controller = Blueprint('mppt_controller', __name__, url_prefix='/mppt', description="Informations sur le contrôleur MPPT")

@mppt_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_controller_data():
    service = MPPTService()
    data_controller: ControllerData = service.read_controller_data()
    if data_controller is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify(data_controller.to_dict()), 200
 