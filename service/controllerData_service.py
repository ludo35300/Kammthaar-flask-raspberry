import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from entity.controllerData_entity import ControllerData
from dto.controllerData_schema import ControllerDataSchema  
from marshmallow.exceptions import ValidationError

class ControllerDataService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les données de status de la batterie.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de charge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel de la batterie.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_controller_data(self) -> ControllerData:
        """
        Récupère les données du contrôleur en temps réel.
        """
        try:
            # Récupération des données brutes
            data = {
                "temperature": self.client.get_controller_temperature(),
                "device_over_temperature": self.client.is_device_over_temperature(),
                "current_device_time": str(self.client.get_rtc())
            }
            # Validation des données via le schéma Marshmallow
            valid_data = ControllerDataSchema().load(data)
            # Création d'une instance de ControllerData avec les données validées
            controller_data = ControllerData(**valid_data)
            return controller_data

        except ValidationError as e:
            logging.error(f"Erreur de validation des données : {e.messages}")
            abort(400, message=f"Erreur de validation des données du contrôleur : {e.messages}")

        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")
 