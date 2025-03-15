import logging
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from constantes.authentification import Authentification
from controller.authentification_controller import authentification_controller
from controller import breadcrumb_controller, batteryParameters_controller,batteryStatus_controller, chargingEquipmentStatus_controller, controllerData_controller, dailyStatistics_controller, dischargingEquipmentStatus_controller, energyStatistics_controller, loadData_controller, solarData_controller
from controller.serveur_controleur import serveur_controller

from service.record_service import RecordService

import threading

# Verrou global pour garantir qu'une seule requête est envoyée à la fois
mppt_lock = threading.Lock()


def create_app():
    logging.basicConfig(level=logging.DEBUG, encoding='utf-8')
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
    CORS(app, origins=["https://api.kammthaar.fr", "*"])
    
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
    api.register_blueprint(breadcrumb_controller.blp_domaine_externe)
    api.register_blueprint(batteryParameters_controller.blp_domaine_externe)
    api.register_blueprint(batteryStatus_controller.blp_domaine_externe)
    api.register_blueprint(chargingEquipmentStatus_controller.blp_domaine_externe)
    api.register_blueprint(controllerData_controller.blp_domaine_externe)
    api.register_blueprint(dailyStatistics_controller.blp_domaine_externe)
    api.register_blueprint(dischargingEquipmentStatus_controller.blp_domaine_externe)
    api.register_blueprint(energyStatistics_controller.blp_domaine_externe)
    api.register_blueprint(loadData_controller.blp_domaine_externe)
    api.register_blueprint(solarData_controller.blp_domaine_externe)
    
    
    api.register_blueprint(serveur_controller)
    api.register_blueprint(authentification_controller)
    
    # Démarrage des enregistrement des données toutes les 10min dans la BDD InfluxDB
    record = RecordService()
    record.start_periodic_recording(interval=600)

    return app

# Création de l'application
app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
