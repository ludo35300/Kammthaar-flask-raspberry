from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from service.batteryParameters_service import BatteryParametersService
from dto.batteryParameters_schema import BatteryParametersSchema

blp_domaine_externe = Blueprint('batteryParameters_controller', 'Paramètres de la batterie', url_prefix='/battery/parameters', description="Récupération des paramètres de la batterie")
batteryParameters_service = BatteryParametersService()

@blp_domaine_externe.route('/realtime')
class BateeryParametersController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, BatteryParametersSchema())  # Sérialisation avec le schéma
    def get(self):
        """
        Récupère les données des paramètres de la batterie en temps réel.
        """
        return batteryParameters_service.read_battery_parameters_data()
