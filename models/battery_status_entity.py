from dataclasses import asdict, dataclass
from models.validators import Validators

@dataclass
class BatteryStatusData:
    wrong_identifaction_for_rated_voltage: bool
    battery_inner_resistence_abnormal: bool
    temperature_warning_status: str
    battery_status: str
    
    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.wrong_identifaction_for_rated_voltage = Validators.validate_boolean(self.wrong_identifaction_for_rated_voltage, "wrong_identifaction_for_rated_voltage")
        self.battery_inner_resistence_abnormal = Validators.validate_boolean(self.battery_inner_resistence_abnormal, "battery_inner_resistence_abnormal")
        self.temperature_warning_status = Validators.validate_string(self.temperature_warning_status, "temperature_warning_status")
        self.battery_status = Validators.validate_string(self.battery_status, "battery_status")

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
        
  