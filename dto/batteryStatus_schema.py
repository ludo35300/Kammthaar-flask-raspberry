from marshmallow import Schema, fields, validates_schema, ValidationError

class BatteryStatusDetailsSchema(Schema):
    """Schéma pour valider les détails du statut de la batterie."""
    wrong_identifaction_for_rated_voltage = fields.Boolean(required=True, error_messages={"required": "L'identification incorrecte pour la tension nominale est requise."})
    battery_inner_resistence_abnormal = fields.Boolean(required=True,error_messages={"required": "Le statut de la résistance interne anormale est requis."})
    temperature_warning_status = fields.String(
        required=True,
        validate=lambda x: x in ["NORMAL", "OVER_TEMP", "LOW_TEMP"],
        error_messages={
            "required": "Le statut de l'alerte température est requis.",
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
    voltage = fields.Float(required=True, error_messages={"required": "La tension (voltage) est obligatoire."})
    current = fields.Float(required=True, error_messages={"required": "Le courant est obligatoire."})
    power = fields.Float(required=True, error_messages={ "required": "La puissance est obligatoire."})
    state_of_charge = fields.Integer(
        required=True,
        validate=lambda x: 0 <= x <= 100,
        error_messages={
            "required": "L'état de charge est obligatoire.",
            "validator_failed": "L'état de charge doit être compris entre 0 et 100 %."
        }
    )
    temperature = fields.Float(required=True, error_messages={"required": "La température est obligatoire."}
    )
    # remote_temperature = fields.Float(required=True, error_messages={"required": "La température distante est obligatoire."})
    status = fields.Nested(
        BatteryStatusDetailsSchema,
        required=True,
        error_messages={"required": "Le statut de la batterie est obligatoire."}
    )

    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"
