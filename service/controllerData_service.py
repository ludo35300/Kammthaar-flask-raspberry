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
        Récupère les données de status de la batterie en temps réel.
        """
        # Récupération des données et création d'une instance de ControllerData
        controller_data = ControllerData(
            temperature = self.client.get_controller_temperature(),
            device_over_temperature = self.client.is_device_over_temperature(),
            current_device_time = self.client.get_rtc()
        )
        # Validation des données via le schéma Marshmallow
        try:
            controller_data = controller_data.to_dict()
            ControllerDataSchema().load(controller_data)  # Validation stricte des données
        except ValidationError as e:
            return abort(400, message=f"Erreur de validation des données du controller : {e.messages}")
        except Exception as e:
            logging.error(f"Erreur interne:", str(e))
            return abort(500, message="Erreur interne du serveur.")
        return controller_data
 