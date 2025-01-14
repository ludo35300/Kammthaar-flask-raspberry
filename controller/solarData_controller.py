from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.solarData_service import SolarDataService
from dto.solarData_schema import SolarDataSchema

blp_domaine_externe = Blueprint('solarData_controller', 'Données du panneau solaire', url_prefix='/solarData', description="Récupération des données du panneau solaire")

# Créer une instance du service
solarData_service = SolarDataService()

@blp_domaine_externe.route('/realtime')
class EnergyStatisticsController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, SolarDataSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données du panneau solaire en temps réel.
        """
        try:
            return solarData_service.read_solar_data()
        except ValidationError as e:
            return {"msg": f"Erreur de validation: {e.messages}"}, 400
        except Exception as e:
            return {"msg": f"Erreur interne du serveur: {str(e)}"}, 500

