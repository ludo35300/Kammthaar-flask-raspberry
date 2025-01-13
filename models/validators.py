
from datetime import datetime, timezone, timedelta

class Validators:
    
    def validate_float(value: float, field_name: str) -> float:
        """Valide que la valeur est un float ou peut être convertie en float."""
        if isinstance(value, float):  # Si c'est déjà un float, on le retourne directement pour éviter les conversions inutiles
            return value
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} doit être un nombre valide.")

    def validate_percentage(value: int, field_name: str) -> int:
        """Valide que le pourcentage est compris entre 0 et 100."""
        if not isinstance(value, int):
            raise ValueError(f"{field_name} doit être un entier valide.")
        if not (0 <= value <= 100):
            raise ValueError(f"{field_name} doit être entre 0 et 100.")
        return value
    

    def validate_string(value: str, field_name: str) -> str:
        """Valide que la valeur est une chaîne de caractères non vide."""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} doit être une chaîne de caractères valide.")
        if not value.strip():
            raise ValueError(f"{field_name} ne doit pas être vide.")
        return str(value)


    def validate_boolean(value, field_name: str) -> bool:
        """Valide que la valeur est un booléen (True ou False)."""
        if not isinstance(value, bool):
            raise ValueError(f"{field_name} doit être un booléen (True ou False).")
        return value

    def validate_date(value, field_name: str) -> str:
        """
        Valide que la valeur est un objet datetime ou une chaîne au format attendu,
        et la retourne sous le format : 'YYYY-MM-DD HH:mm:ss.SSSSSS+00:00'.
        """
        if isinstance(value, datetime):
            # Si la valeur est déjà un datetime, forcer son fuseau horaire à UTC.
            value_datetime = value.astimezone(timezone.utc) - timedelta(hours=1)
        else:
            try:
                # Si la valeur est une chaîne ISO 8601 valide.
                value_datetime = datetime.fromisoformat(value)
            except ValueError:
                try:
                    # Sinon, essaie un format personnalisé.
                    value_datetime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f%z")
                except ValueError:
                    raise ValueError(f"{field_name} doit être une date valide.")

            # Si la date n'a pas de fuseau horaire, ajoutez UTC.
            # Ajuster à UTC-1.
            value_datetime -= timedelta(hours=1)

        # Retourne la date formatée comme demandé.
        return value_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z").replace("+0000", "+00:00")

    def validate_int(value, field_name: str) -> int:
        """Valide que la valeur est un entier ou peut être convertie en entier."""
        if isinstance(value, int):  # Si c'est déjà un int, on le retourne directement pour éviter les conversions inutiles
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} doit être un entier valide.")
        
