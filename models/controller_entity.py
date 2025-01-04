from dataclasses import asdict, dataclass
from datetime import datetime
from models.validators import Validators

@dataclass
class ControllerData:
    controller_temperature: float
    controller_load_amperage: float
    controller_load_power: float
    controller_load_voltage: float
    controller_day_time: bool
    controller_night_time: bool
    controller_date: datetime = datetime.now()
    
    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.controller_temperature = Validators.validate_float(self.controller_temperature, "controller_temperature")
        self.controller_load_amperage = Validators.validate_float(self.controller_load_amperage, "controller_load_amperage")
        self.controller_load_power = Validators.validate_float(self.controller_load_power, "controller_load_power")
        self.controller_load_voltage = Validators.validate_float(self.controller_load_voltage, "controller_load_voltage")
        self.controller_day_time = Validators.validate_boolean(self.controller_day_time, "controller_day_time")
        self.controller_night_time = Validators.validate_boolean(self.controller_night_time, "controller_night_time")
        self.controller_date = Validators.validate_date(self.controller_date, "controller_date")
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        data_dict = asdict(self)
        data_dict["controller_date"] = data_dict["controller_date"].isoformat()
        return data_dict