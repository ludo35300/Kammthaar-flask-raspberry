from marshmallow import Schema, fields

class EnergyStatisticsSchema(Schema):
    """Schéma pour valider les statistiques de génération/consommation d'énergie."""
    consumed_today = fields.Float(required=True, error_messages={"required": "L'énergie consommée aujourd'hui est requise."})
    consumed_this_month = fields.Float(required=True, error_messages={"required": "L'énergie consommée ce mois est requise."})
    consumed_this_year = fields.Float(required=True, error_messages={"required": "L'énergie consommée cette année est requise."})
    total_consumed = fields.Float(required=True, error_messages={"required": "Le total de l'énergie consommée est requis."})
    generated_today = fields.Float(required=True, error_messages={"required": "L'énergie générée aujourd'hui est requise."})
    generated_this_month = fields.Float(required=True, error_messages={"required": "L'énergie générée ce mois est requise."})
    generated_this_year = fields.Float(required=True, error_messages={"required": "L'énergie générée cette année est requise."})
    total_generated = fields.Float(required=True, error_messages={"required": "Le total de l'énergie générée est requis."})
    
    # Autorise les paramètres inconnus mais les exclut
    class Meta:
        unknown = "exclude"
