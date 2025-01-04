from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from models.ps_entity import PSData
from service.ps_service import PSService

ps_controller = Blueprint('ps_controller', __name__, url_prefix='/ps', description="")

@ps_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_ps_data():
    service = PSService()
    data_ps: PSData = service.read_ps_data()
    if data_ps is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify(data_ps.to_dict()), 200