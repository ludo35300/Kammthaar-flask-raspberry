from marshmallow import Schema, fields
    
class LoadDataSchema(Schema):
    voltage = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la tension de la charge."})
    current = fields.Float(required=True, error_messages={"required": "Aucune donnée sur le courant de la charge."})
    power = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la puissance de la charge."})

    # authorise les paramètres inconnus mais les efface
    class Meta:
        unknown = "exclude"
