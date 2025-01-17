from marshmallow import Schema, fields
from datetime import datetime

class BatteryParametersSchema(Schema):
    """Schéma pour valider les données du contrôleur."""
    rated_charging_current = fields.Integer(required=True, error_messages={"required": "Le courant de charge nominal est requis."})
    rated_load_current = fields.Float(required=True, error_messages={"required": "Le courant de charge maximal pour la charge est requis."})
    real_rated_voltage = fields.Integer(required=True, error_messages={"required": "La tension nominale réelle est requise."})
    battery_type = fields.String(required=True, error_messages={"required": "Le type de batterie est requis."})
    battery_capacity = fields.Integer(required=True, error_messages={"required": "La capacité de la batterie est requise."})
    temp_compensation_coefficient = fields.Float(required=True, error_messages={"required": "Le coefficient de compensation thermique est requis."})
    over_voltage_disconnect = fields.Integer(required=True, error_messages={"required": "Le seuil de coupure pour surtension est requis."})
    charging_limit_voltage = fields.Float(required=True, error_messages={"required": "La tension maximale pour la charge est requise."})
    over_voltage_reconnect = fields.Float(required=True, error_messages={"required": "Le seuil de reconnexion après une surtension est requis."})
    equalize_charging_voltage = fields.Float(required=True, error_messages={"required": "La tension de charge d'égalisation est requise."})
    boost_charging_voltage = fields.Float(required=True, error_messages={"required": "La tension de charge rapide est requise."})
    float_charging_voltage = fields.Float(required=True, error_messages={"required": "La tension de charge flottante est requise."})
    boost_reconnect_voltage = fields.Float(required=True, error_messages={"required": "La tension de reconnexion après charge rapide est requise."})
    low_voltage_reconnect = fields.Float(required=True, error_messages={"required": "La tension de reconnexion après basse tension est requise."})
    under_voltage_recover = fields.Float(required=True, error_messages={"required": "Le seuil de récupération après sous-tension est requis."})
    under_voltage_warning = fields.Float(required=True, error_messages={"required": "Le seuil d'avertissement de sous-tension est requis."})
    low_voltage_disconnect = fields.Float(required=True, error_messages={"required": "Le seuil de coupure pour basse tension est requis."})
    discharging_limit_voltage = fields.Float(required=True, error_messages={"required": "La tension limite pour la décharge est requise."})
    battery_rated_voltage = fields.Float(required=True, error_messages={"required": "La tension nominale de la batterie est requise."})
    default_load_mode = fields.String(required=True, error_messages={"required": "Le mode de charge par défaut est requis."})
    equalize_duration = fields.Integer(required=True, error_messages={"required": "La durée de la charge d'égalisation est requise."})
    boost_duration = fields.Integer(required=True, error_messages={"required": "La durée de la charge rapide est requise."})
    battery_discharge = fields.Integer(required=True, error_messages={"required": "La capacité de décharge de la batterie est requise."})
    battery_charge = fields.Integer(required=True, error_messages={"required": "La capacité de charge de la batterie est requise."})
    charging_mode = fields.String(required=True, error_messages={"required": "Le mode de charge est requis."})
    
    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"