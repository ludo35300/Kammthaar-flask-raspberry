from marshmallow import Schema, fields, validates_schema, ValidationError

class DischargingEquipmentErrorsSchema(Schema):
    """Schéma pour valider les erreurs spécifiques de l'équipement de décharge."""
    short_circuit = fields.Boolean(required=True, error_messages={"required": "Le statut du court-circuit est requis."})
    unable_to_discharge = fields.Boolean(required=True, error_messages={"required": "Le statut d'impossibilité de décharge est requis."})
    unable_to_stop_discharging = fields.Boolean(required=True, error_messages={"required": "Le statut d'impossibilité d'arrêter la décharge est requis."})
    output_voltage_abnormal = fields.Boolean(required=True, error_messages={"required": "Le statut de tension de sortie anormale est requis."})
    input_over_voltage = fields.Boolean(required=True, error_messages={"required": "Le statut de survoltage d'entrée est requis."})
    short_circuit_high_voltage_side = fields.Boolean(required=True, error_messages={"required": "Le statut de court-circuit côté haute tension est requis."})
    boost_over_voltage = fields.Boolean(required=True, error_messages={"required": "Le statut de survoltage du boost est requis."})
    output_over_voltage = fields.Boolean(required=True, error_messages={"required": "Le statut de survoltage de sortie est requis."})
    fault = fields.Boolean(required=True, error_messages={"required": "Le statut d'erreur générale est requis."})
    
class DischargingEquipmentStatusSchema(Schema):
    """Schéma pour valider le statut de l'équipement de décharge."""
    input_voltage_status = fields.String(
        required=True,
        validate=lambda x: x in ["NORMAL", "LOW", "HIGH", "NO_ACCESS"],
        error_messages={
            "required": "Le statut de tension d'entrée est requis.",
            "validator_failed": "Le statut doit être 'NORMAL', 'LOW', 'HIGH' ou 'NO_ACCESS'."
        }
    )
    output_power_load = fields.String(
        required=True,
        validate=lambda x: x in ["LIGHT", "MODERATE", "RATED", "OVERLOAD"],
        error_messages={
            "required": "Le statut de la charge de sortie est requis.",
            "validator_failed": "Le statut doit être 'LIGHT', 'MODERATE', 'RATED' ou 'OVERLOAD'."
        }
    )
    running = fields.Boolean(required=True, error_messages={"required": "Le statut de fonctionnement est requis."})
    errors = fields.Nested(
        DischargingEquipmentErrorsSchema,
        required=True,
        error_messages={"required": "Les erreurs de l'équipement de décharge sont obligatoires."}
    )

    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"