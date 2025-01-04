from dataclasses import asdict, dataclass
from models.validators import Validators

@dataclass
class BatteryParametresData:
    rated_charging_current: int
    rated_load_current: float
    real_rated_voltage: str
    battery_type: str
    battery_capacity: int
    temp_compensation_coefficient: float
    over_voltage_disconnect: int
    charging_limit_voltage: float
    over_voltage_reconnect: float
    equalize_charging_voltage: float
    boost_charging_voltage: float
    float_charging_voltage: float
    boost_reconnect_voltage: float
    low_voltage_reconnect: float
    under_voltage_recover: float
    under_voltage_warning: float
    low_voltage_disconnect: float
    discharging_limit_voltage: float
    battery_rated_voltage: float
    default_load_mode: str
    equalize_duration: int
    boost_duration : int
    battery_discharge: int
    battery_charge: int
    charging_mode: str
    
    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.rated_charging_current = Validators.validate_int(self.rated_charging_current, "rated_charging_current")
        self.rated_load_current = Validators.validate_float(self.rated_load_current, "rated_load_current")
        self.real_rated_voltage = Validators.validate_string(self.real_rated_voltage, "real_rated_voltage")
        self.battery_type = Validators.validate_string(self.battery_type, "battery_type")
        self.battery_capacity = Validators.validate_int(self.battery_capacity, "battery_capacity")
        self.temp_compensation_coefficient = Validators.validate_float(self.temp_compensation_coefficient, "temp_compensation_coefficient")
        self.over_voltage_disconnect = Validators.validate_int(self.over_voltage_disconnect, "over_voltage_disconnect")
        self.charging_limit_voltage = Validators.validate_float(self.charging_limit_voltage, "charging_limit_voltage")
        self.over_voltage_reconnect = Validators.validate_float(self.over_voltage_reconnect, "over_voltage_reconnect")
        self.equalize_charging_voltage = Validators.validate_float(self.equalize_charging_voltage, "equalize_charging_voltage")
        self.boost_charging_voltage = Validators.validate_float(self.boost_charging_voltage, "boost_charging_voltage")
        self.float_charging_voltage = Validators.validate_float(self.float_charging_voltage, "float_charging_voltage")
        self.boost_reconnect_voltage = Validators.validate_float(self.boost_reconnect_voltage, "boost_reconnect_voltage")
        self.low_voltage_reconnect = Validators.validate_float(self.low_voltage_reconnect, "low_voltage_reconnect")
        self.under_voltage_recover = Validators.validate_float(self.under_voltage_recover, "under_voltage_recover")
        self.under_voltage_warning = Validators.validate_float(self.under_voltage_warning, "under_voltage_warning")
        self.low_voltage_disconnect = Validators.validate_float(self.low_voltage_disconnect, "low_voltage_disconnect")
        self.discharging_limit_voltage = Validators.validate_float(self.discharging_limit_voltage, "discharging_limit_voltage")
        self.battery_rated_voltage = Validators.validate_string(self.battery_rated_voltage, "battery_rated_voltage")
        self.default_load_mode = Validators.validate_string(self.default_load_mode, "default_load_mode")
        self.equalize_duration = Validators.validate_int(self.equalize_duration, "equalize_duration")
        self.boost_duration = Validators.validate_int(self.boost_duration, "boost_duration")
        self.battery_discharge = Validators.validate_int(self.battery_discharge, "battery_discharge")
        self.battery_charge = Validators.validate_int(self.battery_charge, "battery_charge")
        self.charging_mode = Validators.validate_string(self.charging_mode, "charging_mode")
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
