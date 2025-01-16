from dataclasses import asdict, dataclass
from typing import Dict

@dataclass
class BatteryStatus:
    voltage: float
    current: float
    power: float
    state_of_charge: int
    temperature: float
    # remote_temperature: float
    status: Dict[str, object]  # Statut détaillé de la batterie

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
