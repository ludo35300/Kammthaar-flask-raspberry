from dataclasses import asdict, dataclass
from models.validators import Validators
@dataclass
class StatistiquesData:
    max_battery_voltage_today: float
    min_battery_voltage_today: float
    max_ps_voltage_today: float
    min_ps_voltage_today: float
    consumed_energy_today: float
    consumed_energy_month: float
    consumed_energy_year: float
    consumed_energy_total: float
    generated_energy_today: float
    generated_energy_month: float
    generated_energy_year: float
    generated_energy_total: float
    
    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.max_battery_voltage_today = Validators.validate_float(self.max_battery_voltage_today, "max_battery_voltage_today")
        self.min_battery_voltage_today = Validators.validate_float(self.min_battery_voltage_today, "min_battery_voltage_today")
        self.max_ps_voltage_today = Validators.validate_float(self.max_ps_voltage_today, "max_ps_voltage_today")
        self.min_ps_voltage_today = Validators.validate_float(self.min_ps_voltage_today, "min_ps_voltage_today")
        self.consumed_energy_today = Validators.validate_float(self.consumed_energy_today, "consumed_energy_today")
        self.consumed_energy_month = Validators.validate_float(self.consumed_energy_month, "consumed_energy_month")
        self.consumed_energy_year = Validators.validate_float(self.consumed_energy_year, "consumed_energy_year")
        self.consumed_energy_total = Validators.validate_float(self.consumed_energy_total, "consumed_energy_total")
        self.generated_energy_today = Validators.validate_float(self.generated_energy_today, "generated_energy_today")
        self.generated_energy_month = Validators.validate_float(self.generated_energy_month, "generated_energy_month")
        self.generated_energy_year = Validators.validate_float(self.generated_energy_year, "generated_energy_year")
        self.generated_energy_total = Validators.validate_float(self.generated_energy_total, "generated_energy_total")
        
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)