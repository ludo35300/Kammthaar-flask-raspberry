from marshmallow import Schema, fields, validates, ValidationError

class DailyStatisticsSchema(Schema):
    """Schéma pour valider les statistiques quotidiennes de la batterie."""
    maximum_battery_voltage_today = fields.Float(required=True, error_messages={"required": "La tension maximale de la batterie d'aujourd'hui est requise."})
    minimum_battery_voltage_today = fields.Float(required=True, error_messages={"required": "La tension minimale de la batterie d'aujourd'hui est requise."})
    day_time = fields.Boolean(required=True, error_messages={"required": "L'indicateur 'jour' est requis."})
    night_time = fields.Boolean(required=True, error_messages={"required": "L'indicateur 'nuit' est requis."})

    class Meta:
        unknown = "exclude"
