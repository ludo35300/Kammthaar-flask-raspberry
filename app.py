
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from constantes.authentification import Authentification
from controller.authentification_controller import authentification_controller
from controller.batterie_parametres_controller import batterie_parametres_controller
from controller.ps_controller import ps_controller
from controller.battery_controller import batterie_controller
from controller.battery_status_controller import batterie_status_controller
from controller.mppt_controller import mppt_controller
from controller.statistiques_controller import statistiques_controller
from controller.serveur_controleur import serveur_controller
from service.battery_service import BatterieService
from service.record_service import RecordService


def create_app():
    """
    Crée et configure l'application API Flask.
    
    - Configure CORS pour autoriser les requêtes depuis http://localhost:4200.
    - Initialise Flask-Smorest pour la documentation API avec Swagger.
    - Configure JWT pour la gestion des tokens d'authentification.
    - Enregistre les blueprints des contrôleurs pour structurer l'API.
    - Démarre un service d'enregistrement périodique pour collecter des données MPPT.

    Returns:
        Flask: L'API Flask configurée.
    """
    app = Flask(__name__)
    
    app.debug = True # Dev
    # Configuration CORS
    CORS(app, origins=["http://localhost:4200", "https://api.kammthaar.fr", "https://app.kammthaar.fr", "*"])
    
    # Configuration de la documentation API avec Flask-Smorest
    app.config["API_TITLE"] = "Gestion des Données MPPT"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/api/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # Configuration JWT
    app.config["JWT_SECRET_KEY"] = Authentification.TOKEN
    jwt = JWTManager(app)

    # Initialise l'API
    api = Api(app)

    # Enregistrement des blueprints
    api.register_blueprint(mppt_controller)
    api.register_blueprint(ps_controller)
    api.register_blueprint(batterie_controller)
    api.register_blueprint(batterie_status_controller)
    api.register_blueprint(statistiques_controller)
    api.register_blueprint(batterie_parametres_controller)
    api.register_blueprint(serveur_controller)
    api.register_blueprint(authentification_controller)
    
    record = RecordService()
    record.start_periodic_recording(interval=600)


    return app

# Création de l'application
app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
