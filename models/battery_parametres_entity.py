class BatteryParametresData:
    def __init__(self, rated_charging_current, rated_load_current, real_rated_voltage, battery_type, battery_capacity, 
                 temp_compensation_coefficient, over_voltage_disconnect, charging_limit_voltage, over_voltage_reconnect,
                 equalize_charging_voltage, boost_charging_voltage, float_charging_voltage, boost_reconnect_voltage, 
                 low_voltage_reconnect, under_voltage_recover, under_voltage_warning, low_voltage_disconnect, 
                 discharging_limit_voltage, battery_rated_voltage, default_load_mode, equalize_duration, boost_duration,
                 battery_discharge, battery_charge, charging_mode):

    
        self.rated_charging_current = rated_charging_current
        self.rated_load_current = rated_load_current
        self.real_rated_voltage = real_rated_voltage
        self.battery_type = battery_type
        self.battery_capacity = battery_capacity
        self.temp_compensation_coefficient = temp_compensation_coefficient
        self.over_voltage_disconnect = over_voltage_disconnect
        self.charging_limit_voltage = charging_limit_voltage
        self.over_voltage_reconnect = over_voltage_reconnect
        self.equalize_charging_voltage = equalize_charging_voltage
        self.boost_charging_voltage = boost_charging_voltage
        self.float_charging_voltage = float_charging_voltage
        self.boost_reconnect_voltage = boost_reconnect_voltage
        self.low_voltage_reconnect = low_voltage_reconnect
        self.under_voltage_recover = under_voltage_recover
        self.under_voltage_warning = under_voltage_warning
        self.low_voltage_disconnect = low_voltage_disconnect
        self.discharging_limit_voltage = discharging_limit_voltage
        self.battery_rated_voltage = battery_rated_voltage
        self.default_load_mode = default_load_mode
        self.equalize_duration = equalize_duration
        self.boost_duration = boost_duration
        self.battery_discharge = battery_discharge
        self.battery_charge = battery_charge
        self.charging_mode = charging_mode
        
    def to_dict(self):
        """Convertir l'objet en dictionnaire pour sérialisation JSON."""
        return {
            "rated_charging_current": self.rated_charging_current,
            "rated_load_current": self.rated_load_current,
            "real_rated_voltage": self.real_rated_voltage,
            "battery_type": self.battery_type,
            "battery_capacity": self.battery_capacity,
            "temp_compensation_coefficient": self.temp_compensation_coefficient,
            "over_voltage_disconnect": self.over_voltage_disconnect,
            "charging_limit_voltage": self.charging_limit_voltage,
            "over_voltage_reconnect": self.over_voltage_reconnect,
            "equalize_charging_voltage": self.equalize_charging_voltage,
            "boost_charging_voltage": self.boost_charging_voltage,
            "float_charging_voltage": self.float_charging_voltage,
            "boost_reconnect_voltage": self.boost_reconnect_voltage,
            "low_voltage_reconnect": self.low_voltage_reconnect,
            "under_voltage_recover": self.under_voltage_recover,
            "under_voltage_warning": self.under_voltage_warning,
            "low_voltage_disconnect": self.low_voltage_disconnect,
            "discharging_limit_voltage": self.discharging_limit_voltage,
            "battery_rated_voltage": self.battery_rated_voltage,
            "default_load_mode": self.default_load_mode,
            "equalize_duration": self.equalize_duration,
            "boost_duration": self.boost_duration,
            "battery_discharge": self.battery_discharge,
            "battery_charge": self.battery_charge,
            "charging_mode": self.charging_mode
        }
