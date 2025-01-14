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
        Récupère les données des panneaux solaire en temps réel.
        """
        # Récupération des données et création d'une instance de SolarData
        solar_data = SolarData(
            voltage = self.client.get_solar_voltage(),
            current = self.client.get_solar_current(),
            power = self.client.get_load_power(),
            maximum_voltage_today = self.client.get_maximum_pv_voltage_today(),
            minimum_voltage_today = self.client.get_minimum_pv_voltage_today(),
        )
        # Validation des données via le schéma Marshmallow
        try:
            solar_data = solar_data.to_dict()
            SolarDataSchema().load(solar_data)  # Validation stricte des données
        except ValidationError as e:
            return abort(400, message=f"Erreur de validation des données de charge : {e.messages}")
        except Exception as e:
            logging.error("Erreur interne:", str(e))
            return abort(500, message="Erreur interne du serveur.")
        return solar_data
 