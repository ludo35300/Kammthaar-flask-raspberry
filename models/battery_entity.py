from dataclasses import asdict, dataclass
from models.validators import Validators

@dataclass
class BatteryData:
    battery_voltage: float
    battery_amperage: float
    battery_power: float
    battery_temp: float
    battery_pourcent: int

    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.battery_voltage = Validators.validate_float(self.battery_voltage, "battery_voltage")
        self.battery_amperage = Validators.validate_float(self.battery_amperage, "battery_amperage")
        self.battery_power = Validators.validate_float(self.battery_power, "battery_power")
        self.battery_temp = Validators.validate_float(self.battery_temp, "battery_temp")
        self.battery_pourcent = Validators.validate_percentage(self.battery_pourcent, "battery_pourcent")

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
    