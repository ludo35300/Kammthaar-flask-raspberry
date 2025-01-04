from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from service.serveur_service import ServeurService


serveur_controller = Blueprint('serveur_controller', __name__, url_prefix='/serveur', description="Informations sur le serveur Raspberry Pi")

@serveur_controller.route('/status', methods=['GET'])
@jwt_required()
def get_controller_data():
    serveur = ServeurService()
    return serveur.status()

@serveur_controller.route('/infos', methods=['GET'])
@jwt_required()
def get_serveur_infos():
    serveur = ServeurService()
    return serveur.get_system_info()