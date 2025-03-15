from dataclasses import asdict, dataclass
from typing import Dict

@dataclass
class DischargingEquipmentStatus:
    ''' Entity des données de décharge'''
    input_voltage_status: str
    output_power_load: str
    running: bool
    errors: Dict[str, bool]

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
