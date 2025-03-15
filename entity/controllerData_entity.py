from dataclasses import asdict, dataclass
from datetime import datetime

@dataclass
class ControllerData:
    ''' Entity du controleur MPPT '''
    temperature: float  # Température du contrôleur en °C
    device_over_temperature: bool  # Indique si la température est trop élevée
    current_device_time: datetime  # Heure actuelle du dispositif (format "YYYY-MM-DD HH:MM:SS")

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour une sérialisation JSON."""
        data = asdict(self)
        try:
            # Vérifie si current_device_time est un objet datetime et sérialisation
            if isinstance(self.current_device_time, datetime):
                data["current_device_time"] = self.current_device_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"Erreur lors de la sérialisation de current_device_time: {e}")
        return data
