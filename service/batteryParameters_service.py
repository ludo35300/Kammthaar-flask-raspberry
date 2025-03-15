import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from entity.batteryParameters_entity import BatteryParameters
from dto.batteryParameters_schema import BatteryParametersSchema  
from marshmallow.exceptions import ValidationError

class BatteryParametersService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les paramètres de la batterie.

    Attributes:
        client (EpeverChargeController): Instance du contrôleur Epever permettant d'interagir avec le MPPT via Modbus.
    """
    def __init__(self):
        """
        Initialise le service en configurant une connexion avec le contrôleur MPPT Epever.

        Raises:
            Exception: Si une erreur survient lors de l'initialisation de la connexion au MPPT.
        """
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE) # Connexion au MPPT Epever à l'initialisation

    def read_battery_parameters_data(self) -> BatteryParameters:
        """
        Récupère et valide les paramètres de la batterie à partir du contrôleur Epever.

        Les données récupérées incluent des informations telles que la capacité de la batterie, les tensions
        de charge/décharge, les courants, les durées de charge, et d'autres paramètres liés à la gestion de la batterie.

        Returns:
            BatteryParameters: Objet contenant les paramètres validés de la batterie.

        Raises:
            ValidationError: Si les données récupérées depuis le contrôleur ne respectent pas le schéma défini
                dans `BatteryParametersSchema`.
            HTTPException: Si une erreur survient, une réponse HTTP appropriée est générée avec un statut et un message :
                - 400 (Bad Request) en cas d'erreur de validation.
                - 500 (Internal Server Error) en cas d'erreur interne.
        """
        from app import mppt_lock  # Import du verrou pour éviter les appels simultanés au MPPT
        try:
            with mppt_lock:
                data = {
                    "rated_charging_current":  self.client.get_rated_charging_current(),
                    "rated_load_current": self.client.get_rated_load_current(),
                    "real_rated_voltage": int(self.client.get_battery_rated_voltage().replace("V", "").strip()),
                    "battery_type": self.client.get_battery_type(),
                    "battery_capacity": self.client.get_battery_capacity(),
                    "temp_compensation_coefficient": self.client.get_temperature_compensation_coefficient(),
                    "over_voltage_disconnect": self.client.get_over_voltage_disconnect_voltage(),
                    "charging_limit_voltage": self.client.get_charging_limit_voltage(),
                    "over_voltage_reconnect": self.client.get_over_voltage_reconnect_voltage(),
                    "equalize_charging_voltage": self.client.get_equalize_charging_voltage(),
                    "boost_charging_voltage": self.client.get_boost_charging_voltage(),
                    "float_charging_voltage": self.client.get_float_charging_voltage(),
                    "boost_reconnect_voltage": self.client.get_boost_reconnect_charging_voltage(),
                    "low_voltage_reconnect": self.client.get_low_voltage_reconnect_voltage(),
                    "under_voltage_recover": self.client.get_under_voltage_recover_voltage(),
                    "under_voltage_warning": self.client.get_under_voltage_warning_voltage(),
                    "low_voltage_disconnect": self.client.get_low_voltage_disconnect_voltage(),
                    "discharging_limit_voltage": self.client.get_discharging_limit_voltage(),
                    "battery_rated_voltage": float(self.client.get_battery_rated_voltage().replace("V", "")),
                    "default_load_mode": self.client.get_default_load_on_off_in_manual_mode(),
                    "equalize_duration": self.client.get_equalize_duration(),
                    "boost_duration": self.client.get_boost_duration(),
                    "battery_discharge": self.client.get_battery_discharge(),
                    "battery_charge": self.client.get_battery_charge(),
                    "charging_mode": self.client.get_charging_mode()
                }
            
                valid_data = BatteryParametersSchema().load(data)       # Validation des données via le schéma Marshmallow
                battery_parameters = BatteryParameters(**valid_data)    # Création d'une instance de BatteryParameters avec les données validées
                return battery_parameters
        except ValidationError as e:
            logging.error(f"Erreur de validation des données : {e.messages}")
            abort(400, message=f"Erreur de validation des données des paramètres de la batterie : {e.messages}")

        except Exception as e:
            logging.error(f"Erreur interne : {str(e)}")
            abort(500, message="Erreur interne du serveur.")
    
    
    
    
    

    

    
    
