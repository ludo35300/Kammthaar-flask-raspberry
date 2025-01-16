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
        Récupère les données de charge en temps réel.
        """
        try:
            # Récupération des données brutes
            data = {
                "voltage": self.client.get_load_voltage(),
                "current": self.client.get_load_current(),
                "power": self.client.get_load_power()
            }

            # Validation des données via le schéma Marshmallow
            valid_data = LoadDataSchema().load(data)

            # Création d'une instance de LoadData avec les données validées
            load_data = LoadData(**valid_data)
            return load_data

        except ValidationError as e:
            logging.error(f"Erreur de validation des données : {e.messages}")
            abort(400, message=f"Erreur de validation des données de charge : {e.messages}")

        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")
 