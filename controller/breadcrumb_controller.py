from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from dto.breadcrumb_schema import BreadcrumbSchema
from service import breadcrumb_service
from service.breadcrumb_service import BreadcrumbService

blp_domaine_externe = Blueprint("breadcrumb_controller", "Informations du breadcrumb", description="Récupération de l'heure et du status du jour")

@blp_domaine_externe.route('/breadcrumb')
class BreadcrumbController(MethodView):
    @jwt_required()
    @blp_domaine_externe.response(200, BreadcrumbSchema())  # Sérialisation avec le schéma
    def get(self):
        """
            Récupère les données du breadcrumb.
        """
        return  BreadcrumbService().get_breadcrumb()
