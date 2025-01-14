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
        Récupère les données de dé&charge en temps réel.
        """
        # Récupération des données et création d'une instance de EnergyStatistics
        energy_statistics = EnergyStatistics(
            consumed_today = self.client.get_consumed_energy_today(),
            consumed_this_month = self.client.get_consumed_energy_this_month(),
            consumed_this_year = self.client.get_consumed_energy_this_year(),
            total_consumed = self.client.get_total_consumed_energy(),
            generated_today = self.client.get_generated_energy_today(),
            generated_this_month = self.client.get_generated_energy_this_month(),
            generated_this_year = self.client.get_generated_energy_this_year(),
            total_generated = self.client.get_total_generated_energy()
            
        )
        # Validation des données via le schéma Marshmallow
        try:
            energy_statistics = energy_statistics.to_dict()
            EnergyStatisticsSchema().load(energy_statistics)  # Validation stricte des données
        except ValidationError as e:
            return abort(400, message=f"Erreur de validation des données de charge : {e.messages}")
        except Exception as e:
            logging.error("Erreur interne:", str(e))
            return abort(500, message="Erreur interne du serveur.")
        return energy_statistics
 