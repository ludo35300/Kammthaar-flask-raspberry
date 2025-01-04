from epevermodbus.driver import EpeverChargeController
from flask import abort
from constantes.config import Config
from models.battery_status_entity import BatteryStatusData
from models.discharging_status_entity import DischargerStatusData

class DischargerStatusService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
    
    def read_discharger_status_data(self):
        try:
            # Appel unique pour récupérer toutes les données
            discharger_status_response = self.client.get_battery_status()
        except Exception as e:
            return abort(409, message=str(f"Erreur lors de la lecture des données de status de la batterie : {e}"))
        
        # Extraction des données du dictionnaire avec valeurs par défaut
        input_voltage_status = discharger_status_response.get('input_voltage_status', "NORMAL")
        output_power_load = discharger_status_response.get('output_power_load', "LIGHT")
        short_circuit = discharger_status_response.get('short_circuit', False)
        unable_to_discharge = discharger_status_response.get('unable_to_discharge', False)
        unable_to_stop_discharging = discharger_status_response.get('unable_to_stop_discharging', False)
        output_voltage_abnormal = discharger_status_response.get('output_voltage_abnormal', False)
        input_over_voltage = discharger_status_response.get('input_over_voltage', False)
        short_circuit_in_high_voltage_side = discharger_status_response.get('short_circuit_in_high_voltage_side', False)
        boost_over_voltage = discharger_status_response.get('boost_over_voltage', False)
        output_over_voltage = discharger_status_response.get('output_over_voltage', False)
        fault = discharger_status_response.get('fault', False)
        running = discharger_status_response.get('running', True)
        
        # Création de l'objet `BatteryStatusData`
        discharger_status_data = DischargerStatusData(
            input_voltage_status=input_voltage_status,
            output_power_load=output_power_load,
            short_circuit=short_circuit,
            unable_to_discharge=unable_to_discharge,
            unable_to_stop_discharging=unable_to_stop_discharging,
            output_voltage_abnormal=output_voltage_abnormal,
            input_over_voltage=input_over_voltage,
            short_circuit_in_high_voltage_side=short_circuit_in_high_voltage_side,
            boost_over_voltage=boost_over_voltage,
            output_over_voltage=output_over_voltage,
            fault=fault,
            running=running
        )

        return discharger_status_data
