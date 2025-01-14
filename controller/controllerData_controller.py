from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.controllerData_service import ControllerDataService
from dto.controllerData_schema import ControllerDataSchema

blp_domaine_externe = Blueprint('controllerData_controller', 'Données du controleur', url_prefix='/controller', description="Récupération des données du controlleur MPPT")

# Créer une instance du service
controllerData_service = ControllerDataService()

@blp_domaine_externe.route('/realtime')
class ChargingEquipmentStatusStatusController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, ControllerDataSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données du controller en temps réel.
        """
        try:
            return controllerData_service.read_controller_data()
        except ValidationError as e:
            return {"msg": f"Erreur de validation: {e.messages}"}, 400
        except Exception as e:
            return {"msg": f"Erreur interne du serveur: {str(e)}"}, 500

