
from constantes.config import Config
from epevermodbus.driver import EpeverChargeController
from models.charging_status_entity import ChargingStatusData
from models.controller_entity import ControllerData
import pendulum

class MPPTService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
        
    def read_controller_data(self):
        voltage = self.client.get_load_voltage()
        amperage = self.client.get_load_current()
        power = self.client.get_load_power()
        temperature = self.client.get_controller_temperature()
        day_time = self.client.is_day()
        night_time = self.client.is_night()
        date = self.client.get_rtc()
        # print(pendulum.parse(date))
        data_controller = ControllerData(temperature, amperage, power, 
                                         voltage, day_time, night_time, date)

        return data_controller
    
   
