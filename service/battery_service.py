from datetime import datetime
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from models.battery_entity import BatteryData
from models.battery_status_entity import BatteryStatusData
from service.bdd_service import BDDService

class BatterieService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE) 
        # Instanciation de BDDService InfluxDB
        self.bdd_service = BDDService()
        
    def read_battery_data(self):
        battery_voltage = self.client.get_battery_voltage()
        battery_amperage = self.client.get_battery_current()
        battery_power = self.client.get_battery_power()
        battery_temp = self.client.get_battery_temperature()
        battery_pourcent = self.client.get_battery_state_of_charge()
        
        data_battery = BatteryData(battery_voltage, battery_amperage, battery_power, battery_temp, battery_pourcent)
        # test
        
        
        # test
        return data_battery
    
    def read_battery_status_data(self):
        # Appel unique à get_battery_status pour récupérer toutes les données
        battery_status_response = self.client.get_battery_status()
        
        # Extraction des données du dictionnaire
        wrong_identifaction_for_rated_voltage = battery_status_response.get('wrong_identifaction_for_rated_voltage', False)
        battery_inner_resistence_abnormal = battery_status_response.get('battery_inner_resistence_abnormal', False)
        temperature_warning_status = battery_status_response.get('temperature_warning_status', 'UNKNOWN')
        battery_status = battery_status_response.get('battery_status', 'UNKNOWN')
        
        # Création de l'objet BatteryData avec les valeurs extraites
        data_status_battery = BatteryStatusData(
            wrong_identifaction_for_rated_voltage,
            battery_inner_resistence_abnormal,
            temperature_warning_status,
            battery_status
        )
        
        return data_status_battery
