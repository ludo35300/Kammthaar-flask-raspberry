from marshmallow import Schema, fields

class BreadcrumbSchema(Schema):
    day_time = fields.Boolean(required=True)  # Peut être un String ou un Dict selon le format
    current_device_time = fields.Str(required=True)