import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from marshmallow.exceptions import ValidationError

from entity.loadData_entity import LoadData
from dto.loadData_schema import LoadDataSchema  

class LoadDataService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les statistiques énergétiques.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de décharge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel des statistiques énergétiques.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_load_data(self) -> LoadData:
        """
        Récupère les données de dé&charge en temps réel.
        """
        # Récupération des données et création d'une instance de LoadData
        load_data = LoadData(
            voltage = self.client.get_load_voltage(),
            current = self.client.get_load_current(),
            power = self.client.get_load_power()
        )
        # Validation des données via le schéma Marshmallow
        try:
            load_data = load_data.to_dict()
            LoadDataSchema().load(load_data)  # Validation stricte des données
        except ValidationError as e:
            return abort(400, message=f"Erreur de validation des données de charge : {e.messages}")
        except Exception as e:
            logging.error("Erreur interne:", str(e))
            return abort(500, message="Erreur interne du serveur.")
        return load_data
 