class BatteryStatusData:
    def __init__(self,  wrong_identifaction_for_rated_voltage, battery_inner_resistence_abnormal, temperature_warning_status, battery_status):
        self.wrong_identifaction_for_rated_voltage = wrong_identifaction_for_rated_voltage
        self.battery_inner_resistence_abnormal = battery_inner_resistence_abnormal
        self.temperature_warning_status = temperature_warning_status
        self.battery_status = battery_status

    def to_dict(self):
        """Convertir l'objet en dictionnaire pour sérialisation JSON."""
        return {
            "wrong_identifaction_for_rated_voltage": self.wrong_identifaction_for_rated_voltage,
            "battery_inner_resistence_abnormal": self.battery_inner_resistence_abnormal,
            "temperature_warning_status": self.temperature_warning_status,
            "battery_status": self.battery_status,
        }
        
  