import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from marshmallow.exceptions import ValidationError

from entity.energyStatistics_entity import EnergyStatistics
from dto.energyStatistics_schema import EnergyStatisticsSchema  

class EnergyStatisticsService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les statistiques énergétiques.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de décharge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel des statistiques énergétiques.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_energy_statistics_data(self) -> EnergyStatistics:
        """
        Récupère les données de statistiques d'énergie en temps réel.
        """
        try:
            # Récupération des données brutes
            data = {
                "consumed_today": self.client.get_consumed_energy_today(),
                "consumed_this_month": self.client.get_consumed_energy_this_month(),
                "consumed_this_year": self.client.get_consumed_energy_this_year(),
                "total_consumed": self.client.get_total_consumed_energy(),
                "generated_today": self.client.get_generated_energy_today(),
                "generated_this_month": self.client.get_generated_energy_this_month(),
                "generated_this_year": self.client.get_generated_energy_this_year(),
                "total_generated": self.client.get_total_generated_energy()
            }

            # Validation des données via le schéma Marshmallow
            valid_data = EnergyStatisticsSchema().load(data)

            # Création d'une instance de EnergyStatistics avec les données validées
            energy_statistics = EnergyStatistics(**valid_data)
            return energy_statistics

        except ValidationError as e:
            logging.error(f"Erreur de validation des données : {e.messages}")
            abort(400, message=f"Erreur de validation des données d'énergie : {e.messages}")

        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")
 