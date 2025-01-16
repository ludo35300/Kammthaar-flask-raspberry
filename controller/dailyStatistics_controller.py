from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.dailyStatistics_service import DailyStatisticsService
from dto.dailyStatistics_schema import DailyStatisticsSchema

blp_domaine_externe = Blueprint('dailyStatistics_controller', 'Statistiques journaliers', url_prefix='/statistiques/journalier', description="Récupération des statistiques journaliers")

# Créer une instance du service
dailyStatistics_service = DailyStatisticsService()

@blp_domaine_externe.route('/realtime')
class DailyStatisticsController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, DailyStatisticsSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les statistiques journaliers en temps réel.
        """
        try:
            return dailyStatistics_service.read_daily_statistics_data()
        except ValidationError as e:
            return {"msg": f"Erreur de validation: {e.messages}"}, 400
        except Exception as e:
            return {"msg": f"Erreur interne du serveur: {str(e)}"}, 500

