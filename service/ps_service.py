from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from models.ps_entity import PSData
from service.bdd_service import BDDService

class PSService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
        # Instanciation de BDDService InfluxDB
        self.bdd_service = BDDService()
        
    def read_ps_data(self):
        ps_voltage = int(self.client.get_solar_voltage())
        ps_amperage = round(self.client.get_solar_current(), 1)
        ps_power = round(self.client.get_solar_power(), 1)
        data_ps = PSData(ps_voltage, ps_amperage, ps_power)
        return data_ps