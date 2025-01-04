class ControllerData:
    def __init__(self, controller_temperature, controller_load_amperage, controller_load_power, controller_load_voltage, 
                 controller_day_time, controller_night_time, controller_date):
        self.controller_temperature = controller_temperature
        self.controller_load_amperage = controller_load_amperage
        self.controller_load_power = controller_load_power
        self.controller_load_voltage = controller_load_voltage
        self.controller_day_time = controller_day_time
        self.controller_night_time = controller_night_time
        self.controller_date = controller_date
        
    def to_dict(self):
        """Convertir l'objet en dictionnaire pour sérialisation JSON."""
        return {
            "controller_temperature": self.controller_temperature,
            "controller_load_amperage": self.controller_load_amperage,
            "controller_load_power": self.controller_load_power,
            "controller_load_voltage": self.controller_load_voltage,
            "controller_day_time": self.controller_day_time,
            "controller_night_time": self.controller_night_time,
            "controller_date": self.controller_date.isoformat() if self.controller_date else None,
        }