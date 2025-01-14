from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.dischargingEquipmentStatus_service import DischargingEquipmentStatusService
from dto.dischargingEquipmentStatus_schema import DischargingEquipmentStatusSchema

blp_domaine_externe = Blueprint('dischargingEquipmentStatus_controller', 'Status de décharge', url_prefix='/discharging', description="Récupération des données de la décharge des équipements")

# Créer une instance du service
dischargingEquipmentStatus_service = DischargingEquipmentStatusService()

@blp_domaine_externe.route('/realtime')
class DischargingEquipmentStatusController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, DischargingEquipmentStatusSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données de décharge en temps réel.
        """
        try:
            return dischargingEquipmentStatus_service.read_discharging_equipment_status_data()
        except ValidationError as e:
            return {"msg": f"Erreur de validation: {e.messages}"}, 400
        except Exception as e:
            return {"msg": f"Erreur interne du serveur: {str(e)}"}, 500

