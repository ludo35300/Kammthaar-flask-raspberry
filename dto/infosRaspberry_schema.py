from marshmallow import Schema, fields

class InfosRaspberrySchema(Schema):
    cpu_usage = fields.Float(required=True, error_messages={"required": "L'usage du CPU est requis."})
    memory_usage = fields.Float(required=True, error_messages={"required": "L'usage de la  RAM est requis."})
    disk_usage = fields.Float(required=True, error_messages={"required": "L'usage de l'occupation du disque est requis."})
    temperature = fields.Float(required=True, error_messages={"required": "La température du raspberry est requiss."})
    
    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"