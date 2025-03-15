import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from entity.batteryStatus_entity import BatteryStatus
from dto.batteryStatus_schema import BatteryStatusSchema  
from marshmallow.exceptions import ValidationError



class BatterieStatusService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les données de status de la batterie.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de charge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel de la batterie.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_battery_status_data(self) -> BatteryStatus:
        """
        Récupère les données de status de la batterie en temps réel.
        """
        from app import mppt_lock  # Import du verrou pour éviter les appels simultanés au MPPT
        try:
            with mppt_lock:
                data = {
                    "voltage": self.client.get_battery_voltage(),
                    "current": self.client.get_battery_current(),
                    "power": self.client.get_battery_power(),
                    "state_of_charge": self.client.get_battery_state_of_charge(),
                    "temperature": self.client.get_battery_temperature(),
                    "status": self.client.get_battery_status(),
                }
                valid_data = BatteryStatusSchema().load(data)   # Validation des données via le schéma Marshmallow
                battery_status = BatteryStatus(**valid_data)    # Création d'une instance de BatteryStatus avec les données validées
                return battery_status

        except ValidationError as e:
            logging.error(f"Erreur de validation des données : {e.messages}")
            abort(400, message=f"Erreur de validation des données d'état de la batterie : {e.messages}")
        
        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")
 