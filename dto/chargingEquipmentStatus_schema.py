from marshmallow import Schema, fields, validates_schema, ValidationError

class ChargingEquipmentErrorsSchema(Schema):
    """Schéma pour valider les erreurs spécifiques de l'équipement de charge."""
    charging_mosfet_short_circuit = fields.Boolean(required=True, error_messages={"required": "Le statut du court-circuit du MOSFET de charge est requis."})
    charging_or_anti_reverse_mosfet_open_circuit = fields.Boolean(required=True, error_messages={"required": "Le statut du MOSFET ouvert est requis."})
    anti_reverse_mosfet_short_circuit = fields.Boolean(required=True, error_messages={"required": "Le statut du court-circuit du MOSFET anti-retour est requis."})
    input_over_current = fields.Boolean(required=True, error_messages={"required": "Le statut de surintensité d'entrée est requis."})
    load_over_current = fields.Boolean(required=True, error_messages={"required": "Le statut de surintensité de charge est requis."})
    load_short_circuit = fields.Boolean(required=True, error_messages={"required": "Le statut du court-circuit de charge est requis."})
    load_mosfet_short_circuit = fields.Boolean(required=True, error_messages={"required": "Le statut du court-circuit du MOSFET de charge est requis."})
    disequilibrium_in_three_circuits = fields.Boolean(required=True, error_messages={"required": "Le déséquilibre dans les trois circuits est requis."})
    pv_input_short_circuit = fields.Boolean(required=True, error_messages={"required": "Le statut du court-circuit d'entrée PV est requis."})
    fault = fields.Boolean(required=True, error_messages={"required": "Le statut d'erreur générale est requis."})
    
class ChargingEquipmentStatusSchema(Schema):
    """Schéma pour valider le statut de l'équipement de charge."""
    input_voltage_status = fields.String(
        required=True,
        validate=lambda x: x in ["NORMAL", "NO_INPUT_POWER", "HIGHER_INPUT", "INPUT_VOLTAGE_ERROR"],
        error_messages={
            "required": "Le statut de tension d'entrée est requis.",
            "validator_failed": "Le statut doit être 'NORMAL', 'NO_INPUT_POWER', 'HIGHER_INPUT' ou 'INPUT_VOLTAGE_ERROR'."
        }
    )
    charging_status = fields.String(
        required=True,
        validate=lambda x: x in ["NO_CHARGING", "BOOST", "FLOAT", "EQUALIZATION"],
        error_messages={
            "required": "Le statut de charge est requis.",
            "validator_failed": "Le statut doit être 'NO_CHARGING', 'BOOST', 'FLOAT' ou 'EQUALIZATION'."
        }
    )
    running = fields.Boolean(required=True, error_messages={"required": "Le statut de fonctionnement est requis."})
    errors = fields.Nested(
        ChargingEquipmentErrorsSchema,
        required=True,
        error_messages={"required": "Les erreurs de l'équipement de charge sont obligatoires."}
    )

    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"