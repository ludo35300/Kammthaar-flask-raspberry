class StatistiquesData:
    def __init__(self, max_battery_voltage_today, min_battery_voltage_today, max_ps_voltage_today, min_ps_voltage_today,
                 consumed_energy_today, consumed_energy_month, consumed_energy_year, consumed_energy_total,
                 generated_energy_today, generated_energy_month, generated_energy_year, generated_energy_total):

    
        self.max_battery_voltage_today = max_battery_voltage_today
        self.min_battery_voltage_today = min_battery_voltage_today
        self.max_ps_voltage_today = max_ps_voltage_today
        self.min_ps_voltage_today = min_ps_voltage_today
        self.consumed_energy_today = consumed_energy_today
        self.consumed_energy_month = consumed_energy_month
        self.consumed_energy_year = consumed_energy_year
        self.consumed_energy_total = consumed_energy_total
        self.generated_energy_today = generated_energy_today
        self.generated_energy_month = generated_energy_month
        self.generated_energy_year = generated_energy_year
        self.generated_energy_total = generated_energy_total
        
    def to_dict(self):
        """Convertir l'objet en dictionnaire pour sérialisation JSON."""
        return {
            "max_battery_voltage_today": self.max_battery_voltage_today,
            "min_battery_voltage_today": self.min_battery_voltage_today,
            "max_ps_voltage_today": self.max_ps_voltage_today,
            "min_ps_voltage_today": self.min_ps_voltage_today,
            "consumed_energy_today": self.consumed_energy_today,
            "consumed_energy_month": self.consumed_energy_month,
            "consumed_energy_year": self.consumed_energy_year,
            "consumed_energy_total": self.consumed_energy_total,
            "generated_energy_today": self.generated_energy_today,
            "generated_energy_month": self.generated_energy_month,
            "generated_energy_year": self.generated_energy_year,
            "generated_energy_total": self.generated_energy_total
        }