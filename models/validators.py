
from datetime import datetime

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
        return value


    def validate_boolean(value, field_name: str) -> bool:
        """Valide que la valeur est un booléen (True ou False)."""
        if not isinstance(value, bool):
            raise ValueError(f"{field_name} doit être un booléen (True ou False).")
        return value

    def validate_date(value: str, field_name: str) -> str:
        """Valide que la valeur est une date valide dans le format YYYY-MM-DD."""
        try:
            # Essayer de convertir la chaîne en objet datetime
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"{field_name} doit être une date valide au format YYYY-MM-DD.")
        return value

    def validate_int(value, field_name: str) -> int:
        """Valide que la valeur est un entier ou peut être convertie en entier."""
        if isinstance(value, int):  # Si c'est déjà un int, on le retourne directement pour éviter les conversions inutiles
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} doit être un entier valide.")
        
    def validate_date(value, field_name):
        """Valide que la date est soit un objet datetime, soit une chaîne au format attendu."""
        print(value)
        if isinstance(value, datetime):
            # Si c'est déjà un objet datetime, retourne-le
            return value
        elif isinstance(value, str):
            try:
                # Tente de convertir la chaîne en objet datetime
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError(f"{field_name} doit être une chaîne de caractères au format %Y-%m-%d %H:%M:%S.")
        else:
            raise TypeError(f"{field_name} doit être un objet datetime ou une chaîne au format %Y-%m-%d %H:%M:%S.")