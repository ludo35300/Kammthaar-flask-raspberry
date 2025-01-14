from marshmallow import Schema, fields, validates, ValidationError

class DailyStatisticsSchema(Schema):
    """Schéma pour valider les statistiques quotidiennes de la batterie."""
    maximum_battery_voltage_today = fields.Float(required=True, error_messages={"required": "La tension maximale de la batterie d'aujourd'hui est requise."})
    minimum_battery_voltage_today = fields.Float(required=True, error_messages={"required": "La tension minimale de la batterie d'aujourd'hui est requise."})
    day_time = fields.Boolean(required=True, error_messages={"required": "L'indicateur 'jour' est requis."})
    night_time = fields.Boolean(required=True, error_messages={"required": "L'indicateur 'nuit' est requis."})

    # # Vérifie que l'on a bien une seule période active (jour ou nuit)
    # @validates('day_time')
    # def validate_day_time(self, value, data, **kwargs):
    #     if value and data.get('night_time'):
    #         raise ValidationError("Il ne peut pas être jour et nuit en même temps.")
    
    # @validates('night_time')
    # def validate_night_time(self, value, data, **kwargs):
    #     if value and data.get('day_time'):
    #         raise ValidationError("Il ne peut pas être jour et nuit en même temps.")

    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"
