from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class ControllerDataSchema(Schema):
    """Schéma pour valider les données du contrôleur."""
    temperature = fields.Float(required=True, error_messages={"required": "La température du contrôleur est requise."})
    device_over_temperature = fields.Bool(required=True, error_messages={"required": "L'état de la température du dispositif est requis."})
    current_device_time = fields.String(required=True, error_messages={"required": "L'heure actuelle du dispositif est requise."})

    # Validation pour vérifier que l'heure est bien au format attendu (YYYY-MM-DD HH:MM:SS)
    @validates('current_device_time')
    def validate_time_format(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValidationError("Le format de l'heure est invalide. Utilisez le format 'YYYY-MM-DD HH:MM:SS'.")

    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"
