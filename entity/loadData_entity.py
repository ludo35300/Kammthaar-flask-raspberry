from dataclasses import asdict, dataclass

@dataclass
class LoadData:
    voltage: float
    current: float
    power: float
        
    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)