from dataclasses import asdict, dataclass
from models.validators import Validators

@dataclass
class ChargingStatusData:
    input_voltage_status: str
    charging_mosfet_is_short_circuit: bool
    charging_or_anti_reverse_mosfet_is_open_circuit: bool
    anti_reverse_mosfet_is_short_circuit: bool
    input_over_current: bool
    load_over_current: bool
    load_short_circuit: bool
    load_mosfet_short_circuit: bool
    disequilibrium_in_three_circuits: bool
    pv_input_short_circuit: bool
    charging_status: str
    fault: bool
    running: bool
    
    def __post_init__(self):
        """Effectue les validations après l'initialisation."""
        self.input_voltage_status = Validators.validate_string(self.input_voltage_status, "input_voltage_status")
        self.charging_mosfet_is_short_circuit = Validators.validate_boolean(self.charging_mosfet_is_short_circuit, "charging_mosfet_is_short_circuit")
        self.charging_or_anti_reverse_mosfet_is_open_circuit = Validators.validate_boolean(self.charging_or_anti_reverse_mosfet_is_open_circuit, "charging_or_anti_reverse_mosfet_is_open_circuit")
        self.anti_reverse_mosfet_is_short_circuit = Validators.validate_boolean(self.anti_reverse_mosfet_is_short_circuit, "anti_reverse_mosfet_is_short_circuit")
        self.input_over_current = Validators.validate_boolean(self.input_over_current, "input_over_current")
        self.load_over_current = Validators.validate_boolean(self.load_over_current, "load_over_current")
        self.load_short_circuit = Validators.validate_boolean(self.load_short_circuit, "load_short_circuit")
        self.load_mosfet_short_circuit = Validators.validate_boolean(self.load_mosfet_short_circuit, "load_mosfet_short_circuit")
        self.disequilibrium_in_three_circuits = Validators.validate_boolean(self.disequilibrium_in_three_circuits, "disequilibrium_in_three_circuits")
        self.pv_input_short_circuit = Validators.validate_boolean(self.pv_input_short_circuit, "pv_input_short_circuit")
        self.charging_status = Validators.validate_string(self.charging_status, "charging_status")
        self.fault = Validators.validate_boolean(self.fault, "fault")
        self.running = Validators.validate_boolean(self.running, "running")

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
    
    