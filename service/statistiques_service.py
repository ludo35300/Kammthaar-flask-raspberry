from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from models.statistiques_entity import StatistiquesData
from service.bdd_service import BDDService

class StatistiquesService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
        # Instanciation de BDDService InfluxDB
        self.bdd_service = BDDService()

    def read_statistique_data(self):
        max_battery_voltage_today = float(self.client.get_maximum_battery_voltage_today())
        min_battery_voltage_today = float(self.client.get_minimum_battery_voltage_today())
        max_ps_voltage_today = float(self.client.get_maximum_pv_voltage_today())
        min_ps_voltage_today = float(self.client.get_minimum_pv_voltage_today())
        consumed_energy_today = float(self.client.get_consumed_energy_today())
        consumed_energy_month = float(self.client.get_consumed_energy_this_month())
        consumed_energy_year = float(self.client.get_consumed_energy_this_year())
        consumed_energy_total = float(self.client.get_total_consumed_energy())
        generated_energy_today = float(self.client.get_generated_energy_today())
        generated_energy_month = float(self.client.get_generated_energy_this_month())
        generated_energy_year = float(self.client.get_generated_energy_this_year())
        generated_energy_total = float(self.client.get_total_generated_energy())

        data_statistiques = StatistiquesData(max_battery_voltage_today, min_battery_voltage_today, max_ps_voltage_today, min_ps_voltage_today,
                 consumed_energy_today, consumed_energy_month, consumed_energy_year, consumed_energy_total,
                 generated_energy_today, generated_energy_month, generated_energy_year, generated_energy_total)
        
        return data_statistiques