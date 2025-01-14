import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from marshmallow.exceptions import ValidationError

from entity.chargingEquipmentStatus_entity import ChargingEquipmentStatus
from dto.chargingEquipmentStatus_schema import ChargingEquipmentStatusSchema  

class ChargingEquipmentStatusService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les données de charge.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de charge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel de la charge du système.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_charging_equipment_status_data(self) -> ChargingEquipmentStatus:
        """
        Récupère les données de status de la batterie en temps réel.
        """
        # Récupération des données et création d'une instance de ChargingEquipmentStatus
        charging_status = ChargingEquipmentStatus(
            input_voltage_status = self.client.get_charging_equipment_status()["input_voltage_status"],
            charging_status = self.client.get_charging_equipment_status()["charging_status"],
            running = self.client.get_charging_equipment_status()["running"],
            errors = dict(
                charging_mosfet_short_circuit = self.client.get_charging_equipment_status()["charging_mosfet_is_short_circuit"],
                charging_or_anti_reverse_mosfet_open_circuit = self.client.get_charging_equipment_status()["charging_or_anti_reverse_mosfet_is_open_circuit"],
                anti_reverse_mosfet_short_circuit = self.client.get_charging_equipment_status()["anti_reverse_mosfet_is_short_circuit"],
                input_over_current = self.client.get_charging_equipment_status()["input_over_current"],
                load_over_current = self.client.get_charging_equipment_status()["load_over_current"],
                load_short_circuit = self.client.get_charging_equipment_status()["load_short_circuit"],
                load_mosfet_short_circuit = self.client.get_charging_equipment_status()["load_mosfet_short_circuit"],
                disequilibrium_in_three_circuits = self.client.get_charging_equipment_status()["disequilibrium_in_three_circuits"],
                pv_input_short_circuit = self.client.get_charging_equipment_status()["pv_input_short_circuit"],
                fault = self.client.get_charging_equipment_status()["fault"]
            )
        )
        # Validation des données via le schéma Marshmallow
        try:
            charging_status = charging_status.to_dict()
            ChargingEquipmentStatusSchema().load(charging_status)  # Validation stricte des données
        except ValidationError as e:
            return abort(400, message=f"Erreur de validation des données de charge : {e.messages}")
        except Exception as e:
            logging.error(f"Erreur interne:", str(e))
            return abort(500, message="Erreur interne du serveur.")
        return charging_status
 