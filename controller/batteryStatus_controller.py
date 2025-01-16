from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from service.batteryStatus_service import BatterieStatusService
from dto.batteryStatus_schema import BatteryStatusSchema

blp_domaine_externe = Blueprint('batteryStatus_controller', 'Status de la batterie', url_prefix='/battery', description="Récupération des données de la batterie")

# Créer une instance du service
batteryStatus_service = BatterieStatusService()

@blp_domaine_externe.route('/realtime')
class BatteryStatusController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, BatteryStatusSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données de status de la batterie en temps réel.
        """
        try:
            return batteryStatus_service.read_battery_status_data()
        except ValidationError as e:
            return {"msg": f"Erreur de validation: {e.messages}"}, 400
        except Exception as e:
            return {"msg": f"Erreur interne du serveur: {str(e)}"}, 500

