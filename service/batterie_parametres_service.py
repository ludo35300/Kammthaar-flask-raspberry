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

    def read_battery_parametres_data(self, isConnected):
        
        rated_charging_current =  int(self.client.get_rated_charging_current())
        rated_load_current = float(self.client.get_rated_load_current())
        real_rated_voltage = str(self.client.get_battery_rated_voltage().replace("V", "").strip())
        battery_type = str(self.client.get_battery_type())
        battery_capacity = int(self.client.get_battery_capacity())
        temp_compensation_coefficient = self.client.get_temperature_compensation_coefficient()
        over_voltage_disconnect = int(self.client.get_over_voltage_disconnect_voltage())
        charging_limit_voltage = float(self.client.get_charging_limit_voltage())
        over_voltage_reconnect = float(self.client.get_over_voltage_reconnect_voltage())
        equalize_charging_voltage = float(self.client.get_equalize_charging_voltage())
        boost_charging_voltage = float(self.client.get_boost_charging_voltage())
        float_charging_voltage = float(self.client.get_float_charging_voltage())
        boost_reconnect_voltage = float(self.client.get_boost_reconnect_charging_voltage())
        low_voltage_reconnect = float(self.client.get_low_voltage_reconnect_voltage())
        under_voltage_recover = float(self.client.get_under_voltage_recover_voltage())
        under_voltage_warning = float(self.client.get_under_voltage_warning_voltage())
        low_voltage_disconnect = float(self.client.get_low_voltage_disconnect_voltage())
        discharging_limit_voltage = float(self.client.get_discharging_limit_voltage())
        battery_rated_voltage = float(self.client.get_battery_rated_voltage().replace("V", "").strip())
        default_load_mode = str(self.client.get_default_load_on_off_in_manual_mode())
        equalize_duration = int(self.client.get_equalize_duration())
        boost_duration = int(self.client.get_boost_duration())
        battery_discharge = int(self.client.get_battery_discharge())
        battery_charge = int(self.client.get_battery_charge())
        charging_mode = str(self.client.get_charging_mode())

        battery_parametres = BatteryParametresData(rated_charging_current, rated_load_current, real_rated_voltage, battery_type,
                                                   battery_capacity, temp_compensation_coefficient, over_voltage_disconnect, charging_limit_voltage,
                                                   over_voltage_reconnect, equalize_charging_voltage, boost_charging_voltage, float_charging_voltage,
                                                   boost_reconnect_voltage, low_voltage_reconnect, under_voltage_recover, under_voltage_warning, low_voltage_disconnect, 
                                                   discharging_limit_voltage, battery_rated_voltage, default_load_mode, equalize_duration, boost_duration, battery_discharge, 
                                                   battery_charge, charging_mode)
        
        if(isConnected): self.save_if_changed(battery_parametres)
        return battery_parametres
    
    def save_if_changed(self, new_params: BatteryParametresData):
        # Récupérer les paramètres enregistrés
        stored_params = self.bdd_service.get_battery_parameters()
        # Si aucun paramètre n'est enregistré, sauvegarder directement les nouveaux
        if stored_params is None:
            self.bdd_service.save_battery_parameters(new_params)
            return
        
        # Vérifier s'il y a des différences
        has_changes = any(
            getattr(stored_params, field) != getattr(new_params, field)
            for field in vars(new_params)
        )

        if has_changes:
            # Enregistrement des nouveaux paramètres dans InfluxDB s'il y a eu des changements
            self.bdd_service.save_battery_parameters(new_params)

    

    
    
