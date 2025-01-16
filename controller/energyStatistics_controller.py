from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.energyStatistics_service import EnergyStatisticsService
from dto.energyStatistics_schema import EnergyStatisticsSchema

blp_domaine_externe = Blueprint('energyStatistics_controller', 'Statistiques énergétiques', url_prefix='/energy/statistiques', description="Récupération des statistiques énergétiques")

# Créer une instance du service
energyStatistics_service = EnergyStatisticsService()

@blp_domaine_externe.route('/realtime')
class EnergyStatisticsController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, EnergyStatisticsSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données de charge en temps réel.
        """
        try:
            return energyStatistics_service.read_energy_statistics_data()
        except ValidationError as e:
            return {"msg": f"Erreur de validation: {e.messages}"}, 400
        except Exception as e:
            return {"msg": f"Erreur interne du serveur: {str(e)}"}, 500

