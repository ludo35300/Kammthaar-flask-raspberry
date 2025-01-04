from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from models.battery_entity import BatteryData
from models.battery_status_entity import BatteryStatusData

class BatterieService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les données de la batterie.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de charge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel de la batterie.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_battery_data(self) -> BatteryData:
        """
        Lit et retourne les données de la batterie.

        Récupère les informations suivantes à partir du contrôleur de charge :
        - Tension de la batterie
        - Courant de la batterie
        - Puissance de la batterie
        - Température de la batterie
        - État de charge (SOC)

        Returns:
            BatteryData: Une instance de la classe `BatteryData` contenant les données de la batterie.

        Raises:
            Exception: Si une erreur survient lors de la récupération des données.
        """
        try:
            battery_voltage = self.client.get_battery_voltage()
            battery_amperage = self.client.get_battery_current()
            battery_power = self.client.get_battery_power()
            battery_temp = self.client.get_battery_temperature()
            battery_pourcent = self.client.get_battery_state_of_charge()
        except Exception as e:
            return abort(409, message=str(f"Erreur lors de la lecture des données de la batterie : {e}"))
            
        data_battery = BatteryData(battery_voltage, battery_amperage, battery_power, battery_temp, battery_pourcent)
        return data_battery
    
    
    def read_battery_status_data(self) -> BatteryStatusData:
        """
        Lit et retourne les données d'état de la batterie.

        Récupère les informations suivantes à partir du contrôleur de charge:
        - Identification incorrecte de la tension nominale
        - Résistance interne de la batterie anormale
        - État d'avertissement de la température
        - Statut général de la batterie

        Returns:
            BatteryStatusData: Une instance de la classe `BatteryStatusData` contenant l'état de la batterie.

        Raises:
            Exception: Si une erreur survient lors de la récupération des données.
        """
        try:
            battery_status_response = self.client.get_battery_status() # Appel unique à get_battery_status pour récupérer toutes les données
        except Exception as e:
            return abort(409, message=str(f"Erreur lors de la lecture des données de status de la batterie : {e}"))
        # Extraction des données du dictionnaire
        wrong_identifaction_for_rated_voltage = battery_status_response.get('wrong_identifaction_for_rated_voltage', False)
        battery_inner_resistence_abnormal = battery_status_response.get('battery_inner_resistence_abnormal', False)
        temperature_warning_status = battery_status_response.get('temperature_warning_status', 'UNKNOWN')
        battery_status = battery_status_response.get('battery_status', 'UNKNOWN')

        data_status_battery = BatteryStatusData(
            wrong_identifaction_for_rated_voltage,
            battery_inner_resistence_abnormal,
            temperature_warning_status,
            battery_status
        )
        return data_status_battery
