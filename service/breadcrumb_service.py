
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from dto.breadcrumb_schema import BreadcrumbSchema
from entity.breadcrumb_entity import Breadcrumb
from marshmallow.exceptions import ValidationError
import logging

class BreadcrumbService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les données utiles du breadcrumb.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de charge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel du breadcrumb.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def get_breadcrumb(self):
        """
        Récupère les données du contrôleur en temps réel.
        """
        from app import mppt_lock  # Import du verrou pour éviter les appels simultanés au MPPT
        try:
            with mppt_lock:
                # Récupération des données brutes
                data = Breadcrumb(
                    current_device_time = str(self.client.get_rtc()),
                    day_time = self.client.is_day(),
                )
                # Validation des données via le schéma Marshmallow
                return BreadcrumbSchema().load(data.to_dict()) 


        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")