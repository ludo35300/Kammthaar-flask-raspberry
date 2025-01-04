from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from models.statistiques_entity import StatistiquesData
from service.statistiques_service import StatistiquesService

statistiques_controller = Blueprint('statistiques_controller', __name__, url_prefix='/statistiques', description="")

@statistiques_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_statistiques_data():
    service = StatistiquesService()
    data_statistiques: StatistiquesData = service.read_statistique_data()
    if data_statistiques is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify(data_statistiques.to_dict()), 200