from marshmallow import Schema, fields
    
class LoadDataSchema(Schema):
    """Schéma pour valider les données de consommation d'énergie."""
    voltage = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la tension de la consommation."})
    current = fields.Float(required=True, error_messages={"required": "Aucune donnée sur le courant de la consommation."})
    power = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la puissance de la consommation."})

    # authorise les paramètres inconnus mais les efface
    class Meta:
        unknown = "exclude"
