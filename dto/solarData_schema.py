from marshmallow import Schema, fields
    
class SolarDataSchema(Schema):
    voltage = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la tension des panneaux solaire."})
    current = fields.Float(required=True, error_messages={"required": "Aucune donnée sur le courant des panneaux solaire."})
    power = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la puissance des panneaux solaire."})
    maximum_voltage_today = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la tension maximale des panneaux solaires aujourd'hui."})
    minimum_voltage_today = fields.Float(required=True, error_messages={"required": "Aucune donnée sur la tension minimale des panneaux solaires aujourd'hui."}) 

    # authorise les paramètres inconnus mais les efface
    class Meta:
        unknown = "exclude"
        

