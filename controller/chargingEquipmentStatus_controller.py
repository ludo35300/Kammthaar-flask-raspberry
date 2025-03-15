from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.chargingEquipmentStatus_service import ChargingEquipmentStatusService
from dto.chargingEquipmentStatus_schema import ChargingEquipmentStatusSchema

blp_domaine_externe = Blueprint('chargingEquipmentStatus_controller', 'Status de charge', url_prefix='/charging', description="Récupération des données de la charge des équipements")

# Créer une instance du service
chargingEquipmentStatus_service = ChargingEquipmentStatusService()

@blp_domaine_externe.route('/realtime')
class ChargingEquipmentStatusStatusController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, ChargingEquipmentStatusSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données de charge en temps réel.
        """
        return chargingEquipmentStatus_service.read_charging_equipment_status_data()

