
from constantes.config import Config
from epevermodbus.driver import EpeverChargeController
from models.charging_status_entity import ChargingStatusData
from models.controller_entity import ControllerData
from service.bdd_service import BDDService

class MPPTService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
        # Initialisation de la BDD InfluxDB
        # Instanciation de BDDService
        self.bdd_service = BDDService()

        
        
    def read_controller_data(self):
        controller_load_voltage = self.client.get_load_voltage()
        controller_load_amperage = self.client.get_load_current()
        controller_load_power = self.client.get_load_power()
        controller_load_temperature = self.client.get_controller_temperature()
        controller_day_time = self.client.is_day()
        controller_night_time = self.client.is_night()
        controller_date = self.client.get_rtc()

        data_controller = ControllerData(controller_load_temperature, controller_load_amperage, controller_load_power, 
                                         controller_load_voltage, controller_day_time, controller_night_time, controller_date)

        return data_controller
    
    def read_charging_status(self):
        # Appel à get_charging_equipment_status pour récupérer toutes les données
        charging_equipment_status_response = self.client.get_charging_equipment_status()
        
        # Extraction des données du dictionnaire
        input_voltage_status = charging_equipment_status_response.get('input_voltage_status', 'UNKNOWN')
        charging_mosfet_is_short_circuit = charging_equipment_status_response.get('charging_mosfet_is_short_circuit', False)
        charging_or_anti_reverse_mosfet_is_open_circuit = charging_equipment_status_response.get('charging_or_anti_reverse_mosfet_is_open_circuit', False)
        anti_reverse_mosfet_is_short_circuit = charging_equipment_status_response.get('anti_reverse_mosfet_is_short_circuit', False)
        input_over_current = charging_equipment_status_response.get('input_over_current', False)
        load_over_current = charging_equipment_status_response.get('load_over_current', False)
        load_short_circuit = charging_equipment_status_response.get('load_short_circuit', False)
        load_mosfet_short_circuit = charging_equipment_status_response.get('load_mosfet_short_circuit', False)
        disequilibrium_in_three_circuits = charging_equipment_status_response.get('disequilibrium_in_three_circuits', False)
        pv_input_short_circuit = charging_equipment_status_response.get('pv_input_short_circuit', False)
        charging_status = charging_equipment_status_response.get('charging_status', 'UNKNOWN')
        fault = charging_equipment_status_response.get('fault', False)
        running = charging_equipment_status_response.get('running', False)
        
        # Création de l'objet ChargingEquipmentStatusData avec les valeurs extraites
        data_charging_equipment = ChargingStatusData(
            input_voltage_status,
            charging_mosfet_is_short_circuit,
            charging_or_anti_reverse_mosfet_is_open_circuit,
            anti_reverse_mosfet_is_short_circuit,
            input_over_current,
            load_over_current,
            load_short_circuit,
            load_mosfet_short_circuit,
            disequilibrium_in_three_circuits,
            pv_input_short_circuit,
            charging_status,
            fault,
            running
        )
        
        return data_charging_equipment
