from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.loadData_service import LoadDataService
from dto.loadData_schema import LoadDataSchema

blp_domaine_externe = Blueprint('loadData_controller', 'Données sur la consommation', url_prefix='/loadData', description="Récupération des données de consommation")

# Créer une instance du service
loadData_service = LoadDataService()

@blp_domaine_externe.route('/realtime')
class EnergyStatisticsController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, LoadDataSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données de charge en temps réel.
        """
        try:
            return loadData_service.read_load_data()
        except ValidationError as e:
            return {"msg": f"Erreur de validation: {e.messages}"}, 400
        except Exception as e:
            return {"msg": f"Erreur interne du serveur: {str(e)}"}, 500

