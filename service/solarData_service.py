import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from marshmallow.exceptions import ValidationError

from entity.solarData_entity import SolarData
from dto.solarData_schema import SolarDataSchema  

class SolarDataService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les statistiques énergétiques.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de décharge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel des statistiques énergétiques.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_solar_data(self) -> SolarData:
        """
        Récupère les données des panneaux solaires en temps réel.
        """
        from app import mppt_lock  # Import du verrou pour éviter les appels simultanés au MPPT
        try:
            with mppt_lock:
                # Récupération des données brutes
                raw_data = {
                    "voltage": self.client.get_solar_voltage(),
                    "current": self.client.get_solar_current(),
                    "power": self.client.get_solar_power(),
                    "maximum_voltage_today": self.client.get_maximum_pv_voltage_today(),
                    "minimum_voltage_today": self.client.get_minimum_pv_voltage_today()
                }

                # Validation des données via le schéma Marshmallow
                valid_data = SolarDataSchema().load(raw_data)

                # Création d'une instance de SolarData avec les données validées
                solar_data = SolarData(**valid_data)
                return solar_data

        except ValidationError as e:
            logging.error(f"Erreur de validation des données : {e.messages}")
            abort(400, message=f"Erreur de validation des données solaires : {e.messages}")

        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")
 