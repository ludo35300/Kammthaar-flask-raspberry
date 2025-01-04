class ChargingStatusData:
    def __init__(self, input_voltage_status, charging_mosfet_is_short_circuit, charging_or_anti_reverse_mosfet_is_open_circuit,
                 anti_reverse_mosfet_is_short_circuit, input_over_current, load_over_current, load_short_circuit,
                 load_mosfet_short_circuit, disequilibrium_in_three_circuits, pv_input_short_circuit,
                 charging_status, fault, running):
        self.input_voltage_status = input_voltage_status
        self.charging_mosfet_is_short_circuit = charging_mosfet_is_short_circuit
        self.charging_or_anti_reverse_mosfet_is_open_circuit = charging_or_anti_reverse_mosfet_is_open_circuit
        self.anti_reverse_mosfet_is_short_circuit = anti_reverse_mosfet_is_short_circuit
        self.input_over_current = input_over_current
        self.load_over_current = load_over_current
        self.load_short_circuit = load_short_circuit
        self.load_mosfet_short_circuit = load_mosfet_short_circuit
        self.disequilibrium_in_three_circuits = disequilibrium_in_three_circuits
        self.pv_input_short_circuit = pv_input_short_circuit
        self.charging_status = charging_status
        self.fault = fault
        self.running = running


    def to_dict(self):
        """Convertir l'objet en dictionnaire pour sérialisation JSON."""
        return {
            "input_voltage_status": self.input_voltage_status,
            "charging_mosfet_is_short_circuit": self.charging_mosfet_is_short_circuit,
            "charging_or_anti_reverse_mosfet_is_open_circuit": self.charging_or_anti_reverse_mosfet_is_open_circuit,
            "anti_reverse_mosfet_is_short_circuit": self.anti_reverse_mosfet_is_short_circuit,
            "input_over_current": self.input_over_current,
            "load_over_current": self.load_over_current,
            "load_short_circuit": self.load_short_circuit,
            "load_mosfet_short_circuit": self.load_mosfet_short_circuit,
            "disequilibrium_in_three_circuits": self.disequilibrium_in_three_circuits,
            "pv_input_short_circuit": self.pv_input_short_circuit,
            "charging_status": self.charging_status,
            "fault": self.fault,
            "running": self.running,
            
        }
    
    