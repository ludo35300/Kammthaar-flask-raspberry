from dataclasses import asdict, dataclass

@dataclass
class DailyStatistics:
    ''' Entity des statistiques journalières ??? Inutile, A déplacer (voir schema)'''
    maximum_battery_voltage_today: float
    minimum_battery_voltage_today: float
    day_time: bool
    night_time: bool

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        return asdict(self)
