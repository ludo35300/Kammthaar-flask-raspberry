from dataclasses import asdict, dataclass

@dataclass
class SolarData:
    ''' Entity des données du panneau solaire '''
    voltage: float
    current: float
    power: float
    maximum_voltage_today: float
    minimum_voltage_today: float
    
        
    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)