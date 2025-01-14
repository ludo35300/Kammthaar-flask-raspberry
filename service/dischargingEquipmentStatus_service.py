import logging
from flask_smorest import abort
from epevermodbus.driver import EpeverChargeController
from constantes.config import Config
from marshmallow.exceptions import ValidationError

from entity.dischargingEquipmentStatus_entity import DischargingEquipmentStatus
from dto.dischargingEquipmentStatus_schema import DischargingEquipmentStatusSchema  

class DischargingEquipmentStatusService:
    """
    Service pour interagir avec le contrôleur de charge Epever et récupérer les données de charge.

    Cette classe utilise la bibliothèque `epevermodbus` pour se connecter au contrôleur de décharge via Modbus
    et fournit des méthodes pour récupérer les données en temps réel de la décharge du système.
    """
    def __init__(self):
        self.client = EpeverChargeController(Config.MODBUS_PORT, Config.MODBUS_SLAVE)  # Connexion au MPPT Epever
    
    def read_discharging_equipment_status_data(self) -> DischargingEquipmentStatus:
        """
        Récupère les données de dé&charge en temps réel.
        """
        # Récupération des données et création d'une instance de DischargingEquipmentStatus
        discharging_status = DischargingEquipmentStatus(
            input_voltage_status = self.client.get_discharging_equipment_status()["input_voltage_status"],
            output_power_load = self.client.get_discharging_equipment_status()["output_power_load"],
            running = self.client.get_discharging_equipment_status()["running"],
            errors = dict(
                short_circuit = self.client.get_discharging_equipment_status()["short_circuit"],
                unable_to_discharge = self.client.get_discharging_equipment_status()["unable_to_discharge"],
                unable_to_stop_discharging = self.client.get_discharging_equipment_status()["unable_to_stop_discharging"],
                output_voltage_abnormal = self.client.get_discharging_equipment_status()["output_voltage_abnormal"],
                input_over_voltage = self.client.get_discharging_equipment_status()["input_over_voltage"],
                short_circuit_high_voltage_side = self.client.get_discharging_equipment_status()["short_circuit_in_high_voltage_side"],
                boost_over_voltage = self.client.get_discharging_equipment_status()["boost_over_voltage"],
                output_over_voltage = self.client.get_discharging_equipment_status()["output_over_voltage"],
                fault = self.client.get_discharging_equipment_status()["fault"]
            )
        )
        # Validation des données via le schéma Marshmallow
        try:
            discharging_status = discharging_status.to_dict()
            DischargingEquipmentStatusSchema().load(discharging_status)  # Validation stricte des données
        except ValidationError as e:
            return abort(400, message=f"Erreur de validation des données de charge : {e.messages}")
        except Exception as e:
            logging.error(f"Erreur interne:", str(e))
            return abort(500, message="Erreur interne du serveur.")
        return discharging_status
 