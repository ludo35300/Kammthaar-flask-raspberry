
from constantes.config import Config
from epevermodbus.driver import EpeverChargeController
from models.charging_status_entity import ChargingStatusData
from models.controller_entity import ControllerData

class MPPTService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
        
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
    
