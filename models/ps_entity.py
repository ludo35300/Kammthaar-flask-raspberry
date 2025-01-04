from dataclasses import asdict, dataclass
from models.validators import Validators

@dataclass
class PSData:
    ps_voltage: float
    ps_amperage: float
    ps_power: float
    
    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.ps_voltage = Validators.validate_int(self.ps_voltage, "ps_voltage")
        self.ps_amperage = Validators.validate_float(self.ps_amperage, "ps_amperage")
        self.ps_power = Validators.validate_float(self.ps_power, "ps_power")
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
