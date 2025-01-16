from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class ControllerDataSchema(Schema):
    """Schéma pour valider les données du contrôleur."""
    temperature = fields.Float(required=True, error_messages={"required": "La température du contrôleur est requise."})
    device_over_temperature = fields.Bool(required=True, error_messages={"required": "L'état de la température du dispositif est requis."})
    current_device_time = fields.DateTime( required=True, error_messages={"required": "L'heure actuelle du dispositif est requise."})

    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"
