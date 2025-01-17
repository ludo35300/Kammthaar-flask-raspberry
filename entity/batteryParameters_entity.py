from dataclasses import asdict, dataclass

@dataclass
class BatteryParameters:
    rated_charging_current: int
    rated_load_current: float
    real_rated_voltage: int
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
    
    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)