from dataclasses import asdict, dataclass
from typing import Dict

@dataclass
class ChargingEquipmentStatus:
    ''' Entity des données de charge'''
    input_voltage_status: str
    charging_status: str
    running: bool
    errors: Dict[str, bool]

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
