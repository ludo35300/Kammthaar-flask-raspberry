from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from service.serveur_service import ServeurService


serveur_controller = Blueprint('serveur_controller', __name__, url_prefix='/serveur', description="Informations sur le serveur Raspberry Pi")
serveur = ServeurService()


@serveur_controller.route('/infos', methods=['GET'])
@jwt_required()
def get_serveur_infos():
    return serveur.get_system_info()