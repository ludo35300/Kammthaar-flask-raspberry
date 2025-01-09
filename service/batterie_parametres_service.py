from datetime import datetime
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from models.battery_parametres_entity import BatteryParametresData
from service.bdd_service import BDDService

class BatterieParametresService:
    def __init__(self):
        # Connexion au MPPT Epever
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)
        # Instanciation de BDDService InfluxDB
        self.bdd_service = BDDService()

    def read_battery_parametres_data(self) -> BatteryParametresData:
        rated_charging_current =  self.client.get_rated_charging_current()
        rated_load_current = self.client.get_rated_load_current()
        real_rated_voltage = self.client.get_battery_rated_voltage().replace("V", "").strip()
        battery_type = self.client.get_battery_type()
        battery_capacity = self.client.get_battery_capacity()
        temp_compensation_coefficient = self.client.get_temperature_compensation_coefficient()
        over_voltage_disconnect = self.client.get_over_voltage_disconnect_voltage()
        charging_limit_voltage = self.client.get_charging_limit_voltage()
        over_voltage_reconnect = self.client.get_over_voltage_reconnect_voltage()
        equalize_charging_voltage = self.client.get_equalize_charging_voltage()
        boost_charging_voltage = self.client.get_boost_charging_voltage()
        float_charging_voltage = self.client.get_float_charging_voltage()
        boost_reconnect_voltage = self.client.get_boost_reconnect_charging_voltage()
        low_voltage_reconnect = self.client.get_low_voltage_reconnect_voltage()
        under_voltage_recover = self.client.get_under_voltage_recover_voltage()
        under_voltage_warning = self.client.get_under_voltage_warning_voltage()
        low_voltage_disconnect = self.client.get_low_voltage_disconnect_voltage()
        discharging_limit_voltage = self.client.get_discharging_limit_voltage()
        battery_rated_voltage = float(self.client.get_battery_rated_voltage().replace("V", ""))
        default_load_mode = self.client.get_default_load_on_off_in_manual_mode()
        equalize_duration = self.client.get_equalize_duration()
        boost_duration = self.client.get_boost_duration()
        battery_discharge = self.client.get_battery_discharge()
        battery_charge = self.client.get_battery_charge()
        charging_mode = self.client.get_charging_mode()
        
        battery_parametres = BatteryParametresData(rated_charging_current, rated_load_current, real_rated_voltage, battery_type,
                                                   battery_capacity, temp_compensation_coefficient, over_voltage_disconnect, charging_limit_voltage,
                                                   over_voltage_reconnect, equalize_charging_voltage, boost_charging_voltage, float_charging_voltage,
                                                   boost_reconnect_voltage, low_voltage_reconnect, under_voltage_recover, under_voltage_warning, low_voltage_disconnect, 
                                                   discharging_limit_voltage, battery_rated_voltage, default_load_mode, equalize_duration, boost_duration, battery_discharge, 
                                                   battery_charge, charging_mode)

        return battery_parametres
    
    
    
    
    

    

    
    
