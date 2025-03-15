from dataclasses import asdict, dataclass

@dataclass
class EnergyStatistics:
    ''' Entity des statistiques énergétiques '''
    consumed_today: float
    consumed_this_month: float
    consumed_this_year: float
    total_consumed: float
    generated_today: float
    generated_this_month: float
    generated_this_year: float
    total_generated: float

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
