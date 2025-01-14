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
        # Récupération des données et création d'une instance de BatteryStatus
        battery_status = BatteryStatus(
            voltage = self.client.get_battery_voltage(),
            current = self.client.get_battery_current(),
            power = self.client.get_battery_power(),
            state_of_charge = self.client.get_battery_state_of_charge(),
            temperature = self.client.get_battery_temperature(),
            # remote_temperature= self.client.get_remote_battery_temperature(),
            status=self.client.get_battery_status()  # Statut détaillé de la batterie
        )
        # Validation des données via le schéma Marshmallow
        try:
            battery_status = battery_status.to_dict()
            BatteryStatusSchema().load(battery_status)  # Validation stricte des données
        except ValidationError as e:
            return abort(400, message=f"Erreur de validation des données d'état de la batterie : {e.messages}")
        except Exception as e:
            logging.error(f"Erreur interne:", str(e))
            return abort(500, message="Erreur interne du serveur.")
        return battery_status
 