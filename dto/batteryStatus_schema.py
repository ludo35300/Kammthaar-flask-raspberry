from marshmallow import Schema, fields, validates_schema, ValidationError

class BatteryDetailsSchema(Schema):
    """Schéma pour valider les détails du statut de la batterie."""
    wrong_identifaction_for_rated_voltage = fields.Boolean(
        required=True, 
        error_messages={"required": "L'identification incorrecte pour la tension nominale de la batterie est requise."})
    battery_inner_resistence_abnormal = fields.Boolean(
        required=True,
        error_messages={"required": "Le statut de la résistance interne anormale de la batterie est requis."})
    temperature_warning_status = fields.String(
        required=True,
        validate=lambda x: x in ["NORMAL", "OVER_TEMP", "LOW_TEMP"],
        error_messages={
            "required": "Le statut de l'alerte température de la batterie est requis.",
            "validator_failed": "Le statut doit être 'NORMAL', 'OVER_TEMP' ou 'LOW_TEMP'."
        }
    )
    battery_status = fields.String(
        required=True,
        validate=lambda x: x in ["NORMAL", "OVER_VOLTAGE", "UNDER_VOLTAGE", "OVER_DISCHARGE","FAULT"],
        error_messages={
            "required": "Le statut général de la batterie est requis.",
            "validator_failed": "Le statut doit être 'NORMAL', 'OVER_VOLTAGE', 'UNDER_VOLTAGE', 'OVER_DISCHARGE' ou 'FAULT'."
        }
    )
    
class BatteryStatusSchema(Schema):
    """Schéma pour valider les données du statut de la batterie."""
    voltage = fields.Float(required=True, error_messages={"required": "La tension (voltage) de la batterie est obligatoire."})
    current = fields.Float(required=True, error_messages={"required": "Le courant de la batterie est obligatoire."})
    power = fields.Float(required=True, error_messages={ "required": "La puissance de la batterie est obligatoire."})
    state_of_charge = fields.Integer(
        required=True,
        validate=lambda x: 0 <= x <= 100,
        error_messages={
            "required": "Le pourcentage de charge de la batterie est obligatoire.",
            "validator_failed": "Le pourcentage de charge de la batterie doit être compris entre 0 et 100 %."
        }
    )
    temperature = fields.Float(required=True, error_messages={"required": "La température de la batterie est obligatoire."}
    )
    status = fields.Nested(
        BatteryDetailsSchema,
        required=True,
        error_messages={"required": "Le détail du statut de la batterie est obligatoire."}
    )
    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"
