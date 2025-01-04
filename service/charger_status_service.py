from epevermodbus.driver import EpeverChargeController
from flask import abort
from constantes.config import Config
from models.charging_status_entity import ChargingStatusData

class ChargingStatusService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
        
    def read_charging_status_data(self):
        try:
            charging_status_response = self.client.get_charging_equipment_status() # Appel unique à get_charging_equipment_status pour récupérer toutes les données
        except Exception as e:
            return abort(409, message=str(f"Erreur lors de la lecture des données de status de la batterie : {e}"))
        # Extraction des données du dictionnaire
        input_voltage_status = charging_status_response.get('input_voltage_status', "NORMAL")
        charging_mosfet_is_short_circuit = charging_status_response.get('charging_mosfet_is_short_circuit', False)
        charging_or_anti_reverse_mosfet_is_open_circuit = charging_status_response.get('charging_or_anti_reverse_mosfet_is_open_circuit', False)
        anti_reverse_mosfet_is_short_circuit = charging_status_response.get('anti_reverse_mosfet_is_short_circuit', False)
        input_over_current = charging_status_response.get('input_over_current', False)
        load_over_current = charging_status_response.get('load_over_current', False)
        load_short_circuit = charging_status_response.get('load_short_circuit', False)
        load_mosfet_short_circuit = charging_status_response.get('load_mosfet_short_circuit', False)
        disequilibrium_in_three_circuits = charging_status_response.get('disequilibrium_in_three_circuits', False)
        pv_input_short_circuit = charging_status_response.get('pv_input_short_circuit', False)
        charging_status = charging_status_response.get('charging_status', "NO_CHARGING")
        fault = charging_status_response.get('fault', False)
        running = charging_status_response.get('running', False)
        
        
        data_status_charging = ChargingStatusData(
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
            running,
        )
        return data_status_charging