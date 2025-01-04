from dataclasses import dataclass, asdict
from models.validators import Validators  # Supposant que vous utilisez le même système de Validators.

@dataclass
class DischargerStatusData:
    input_voltage_status: str
    output_power_load: str
    short_circuit: bool
    unable_to_discharge: bool
    unable_to_stop_discharging: bool
    output_voltage_abnormal: bool
    input_over_voltage: bool
    short_circuit_in_high_voltage_side: bool
    boost_over_voltage: bool
    output_over_voltage: bool
    fault: bool
    running: bool

    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.input_voltage_status = Validators.validate_string(self.input_voltage_status, "input_voltage_status")
        self.output_power_load = Validators.validate_string(self.output_power_load, "output_power_load")
        self.short_circuit = Validators.validate_boolean(self.short_circuit, "short_circuit")
        self.unable_to_discharge = Validators.validate_boolean(self.unable_to_discharge, "unable_to_discharge")
        self.unable_to_stop_discharging = Validators.validate_boolean(self.unable_to_stop_discharging, "unable_to_stop_discharging")
        self.output_voltage_abnormal = Validators.validate_boolean(self.output_voltage_abnormal, "output_voltage_abnormal")
        self.input_over_voltage = Validators.validate_boolean(self.input_over_voltage, "input_over_voltage")
        self.short_circuit_in_high_voltage_side = Validators.validate_boolean(self.short_circuit_in_high_voltage_side, "short_circuit_in_high_voltage_side")
        self.boost_over_voltage = Validators.validate_boolean(self.boost_over_voltage, "boost_over_voltage")
        self.output_over_voltage = Validators.validate_boolean(self.output_over_voltage, "output_over_voltage")
        self.fault = Validators.validate_boolean(self.fault, "fault")
        self.running = Validators.validate_boolean(self.running, "running")

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
