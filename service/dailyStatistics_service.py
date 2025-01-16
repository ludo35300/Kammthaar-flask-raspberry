from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from marshmallow.exceptions import ValidationError

from entity.dailyStatistics_entity import DailyStatistics
from dto.dailyStatistics_schema import DailyStatisticsSchema  


class DailyStatisticsService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les statistiques journalier.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de charge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel de la batterie.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_daily_statistics_data(self) -> DailyStatistics:
        """
        Récupère les données de statistiques journalières en temps réel.
        """
        try:
            # Récupération des données brutes
            data = {
                "maximum_battery_voltage_today": self.client.get_maximum_battery_voltage_today(),
                "minimum_battery_voltage_today": self.client.get_minimum_battery_voltage_today(),
                "day_time": self.client.is_day(),
                "night_time": self.client.is_night(),
            }
            # Validation des données via le schéma Marshmallow
            valid_data = DailyStatisticsSchema().load(data)

            # Création d'une instance de DailyStatistics avec les données validées
            daily_statistics_data = DailyStatistics(**valid_data)
            return daily_statistics_data

        except ValidationError as e:
            logging.error(f"Erreur de validation des données : {e.messages}")
            abort(400, message=f"Erreur de validation des statistiques journalières : {e.messages}")

        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")
 