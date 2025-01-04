from datetime import datetime
import logging
import influxdb_client, time, os
from flask import json
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from constantes.config import Config
from models.battery_entity import BatteryData
from models.battery_parametres_entity import BatteryParametresData
from models.battery_status_entity import BatteryStatusData
from models.ps_entity import PSData
from models.controller_entity import ControllerData
from models.statistiques_entity import StatistiquesData


class BDDService:    
    def __init__(self):
        # Initialisation de la BDD InfluxDB
        try:
            self.client = influxdb_client.InfluxDBClient(url=Config.INFLUXDB_URL, token=Config.INFLUXDB_TOKEN, org=Config.INFLUXDB_ORG, timeout=5000)
            logging.basicConfig(level=logging.DEBUG)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
        except Exception as e:
            print(f"Erreur de connexion à InfluxDB 2.0': {e}")

 
        
    def save_battery_data(self, battery_data: BatteryData, timestamp):
        point = Point("battery_data") \
            .tag("device", "battery") \
            .field("battery_voltage", float(battery_data.battery_voltage)) \
            .field("battery_amperage", float(battery_data.battery_amperage)) \
            .field("battery_power", float(battery_data.battery_power)) \
            .field("battery_temp", float(battery_data.battery_temp)) \
            .field("battery_pourcent", battery_data.battery_pourcent) \
            .time(timestamp)
        self.write_api.write(bucket=Config.INFLUXDB_BUCKET, org=Config.INFLUXDB_ORG, record=point)
        logging.info("Données de la batterie sauvegardées avec succès")
        time.sleep(1) 
        
    def save_battery_status_data(self, battery_status_data: BatteryStatusData, timestamp):
        try:
            point = Point("battery_status_data") \
                .tag("device", "battery_status_data") \
                .field("wrong_identifaction_for_rated_voltage", bool(battery_status_data.wrong_identifaction_for_rated_voltage)) \
                .field("battery_inner_resistence_abnormal", bool(battery_status_data.battery_inner_resistence_abnormal)) \
                .field("temperature_warning_status", str(battery_status_data.temperature_warning_status)) \
                .field("battery_status", str(battery_status_data.battery_status)) \
                .time(timestamp)
            self.write_api.write(bucket=Config.INFLUXDB_BUCKET, record=point)
            time.sleep(1)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des données de status de la batterie': {e}")

    def save_ps_data(self, ps_data: PSData, timestamp):
        point = Point("ps_data") \
            .tag("device", "solar_panel") \
            .field("voltage", ps_data.ps_voltage) \
            .field("amperage", float(ps_data.ps_amperage)) \
            .field("power", ps_data.ps_power) \
            .time(timestamp)
        self.write_api.write(bucket=Config.INFLUXDB_BUCKET, record=point)
        logging.info("Données du panneau solaire sauvegardées avec succès")
        time.sleep(1) 

    def save_controller_data(self, controller_data: ControllerData, timestamp):
        point = Point("controller_data") \
            .tag("device", "controller_data") \
            .field("voltage", float(controller_data.controller_load_voltage)) \
            .field("amperage", float(controller_data.controller_load_amperage)) \
            .field("power", float(controller_data.controller_load_power))\
            .field("temperature", float(controller_data.controller_temperature))\
            .field("day_time", controller_data.controller_day_time)\
            .field("night_time", controller_data.controller_night_time) \
            .time(timestamp)
        self.write_api.write(bucket=Config.INFLUXDB_BUCKET, record=point)
        logging.info("Données du controlleur MPPT sauvegardées avec succès")
        time.sleep(1) 

    def save_statistiques_data(self, statistiques_data: StatistiquesData, timestamp):
        point = Point("statistiques_data") \
            .tag("device", "statistiques_data") \
            .field("max_battery_voltage_today", statistiques_data.max_battery_voltage_today)\
            .field("min_battery_voltage_today", statistiques_data.min_battery_voltage_today)\
            .field("max_ps_voltage_today", statistiques_data.max_ps_voltage_today)\
            .field("min_ps_voltage_today", statistiques_data.min_ps_voltage_today)\
            .field("consumed_energy_today", statistiques_data.consumed_energy_today)\
            .field("consumed_energy_month", statistiques_data.consumed_energy_month)\
            .field("consumed_energy_year", statistiques_data.consumed_energy_year)\
            .field("consumed_energy_total", statistiques_data.consumed_energy_total)\
            .field("generated_energy_today", statistiques_data.generated_energy_today)\
            .field("generated_energy_month", statistiques_data.generated_energy_month)\
            .field("generated_energy_year", statistiques_data.generated_energy_year)\
            .field("generated_energy_total", statistiques_data.generated_energy_total) \
            .time(timestamp)
        self.write_api.write(bucket=Config.INFLUXDB_BUCKET, record=point)
        logging.info("Données des satistiques sauvegardées avec succès")
        time.sleep(1) 

    
    def save_battery_parameters(self, battery_parametres: BatteryParametresData, timestamp):
        point = Point("batterie_parametres") \
            .field("rated_charging_current", int(battery_parametres.rated_charging_current)) \
            .field("rated_load_current", float(battery_parametres.rated_load_current)) \
            .field("real_rated_voltage", str(battery_parametres.real_rated_voltage.replace("V", "").strip())) \
            .field("battery_type", str(battery_parametres.battery_type)) \
            .field("battery_capacity", int(battery_parametres.battery_capacity)) \
            .field("temp_compensation_coefficient", float(battery_parametres.temp_compensation_coefficient)) \
            .field("over_voltage_disconnect", int(battery_parametres.over_voltage_disconnect)) \
            .field("charging_limit_voltage", float(battery_parametres.charging_limit_voltage)) \
            .field("over_voltage_reconnect", float(battery_parametres.over_voltage_reconnect)) \
            .field("equalize_charging_voltage", float(battery_parametres.equalize_charging_voltage)) \
            .field("boost_charging_voltage", float(battery_parametres.boost_charging_voltage)) \
            .field("float_charging_voltage", float(battery_parametres.float_charging_voltage)) \
            .field("boost_reconnect_voltage", float(battery_parametres.boost_reconnect_voltage)) \
            .field("low_voltage_reconnect", float(battery_parametres.low_voltage_reconnect)) \
            .field("under_voltage_recover", float(battery_parametres.under_voltage_recover)) \
            .field("under_voltage_warning", float(battery_parametres.under_voltage_warning)) \
            .field("low_voltage_disconnect", float(battery_parametres.low_voltage_disconnect)) \
            .field("discharging_limit_voltage", float(battery_parametres.discharging_limit_voltage)) \
            .field("battery_rated_voltage", float(battery_parametres.real_rated_voltage.replace("V", "").strip())) \
            .field("default_load_mode", str(battery_parametres.default_load_mode)) \
            .field("equalize_duration", int(battery_parametres.equalize_duration)) \
            .field("boost_duration", int(battery_parametres.boost_duration)) \
            .field("battery_discharge", int(battery_parametres.battery_discharge)) \
            .field("battery_charge", int(battery_parametres.battery_charge)) \
            .field("charging_mode", str(battery_parametres.charging_mode)) \
            .time(timestamp)

        # Écriture dans la base de données
        self.write_api.write(bucket=Config.INFLUXDB_BUCKET, org=Config.INFLUXDB_ORG, record=point)


    #TODO A METTRE DANS BATTERIE PARAMETRES SERVICE
    def get_battery_parameters(self):

        # Construire la requête pour récupérer les paramètres de batterie
        query = f'''
        from(bucket: "{Config.INFLUXDB_BUCKET}")
        |> range(start: -1d)   // Durée de recherche
        |> filter(fn: (r) => r._measurement == "batterie_parametres")
        |> last()              // Dernier enregistrement
        '''

        try:
            # Exécuter la requête InfluxDB
            result = self.query_api.query(org=Config.INFLUXDB_ORG, query=query)

            # Initialiser un dictionnaire pour stocker les valeurs de paramètres
            params = {}

            # Parcourir tous les enregistrements pour remplir le dictionnaire de paramètres
            for table in result:
                for record in table.records:
                    field = record.get_field()  # Nom du champ
                    value = record.get_value()  # Valeur du champ
                    params[field] = value

            # Créer l'instance de BatteryParametresData avec les paramètres récupérés
            battery_params = BatteryParametresData(
                rated_charging_current=params.get("rated_charging_current"),
                rated_load_current=params.get("rated_load_current"),
                real_rated_voltage=params.get("real_rated_voltage"),
                battery_type=params.get("battery_type"),
                battery_capacity=params.get("battery_capacity"),
                temp_compensation_coefficient=params.get("temp_compensation_coefficient"),
                over_voltage_disconnect=params.get("over_voltage_disconnect"),
                charging_limit_voltage=params.get("charging_limit_voltage"),
                over_voltage_reconnect=params.get("over_voltage_reconnect"),
                equalize_charging_voltage=params.get("equalize_charging_voltage"),
                boost_charging_voltage=params.get("boost_charging_voltage"),
                float_charging_voltage=params.get("float_charging_voltage"),
                boost_reconnect_voltage=params.get("boost_reconnect_voltage"),
                low_voltage_reconnect=params.get("low_voltage_reconnect"),
                under_voltage_recover=params.get("under_voltage_recover"),
                under_voltage_warning=params.get("under_voltage_warning"),
                low_voltage_disconnect=params.get("low_voltage_disconnect"),
                discharging_limit_voltage=params.get("discharging_limit_voltage"),
                battery_rated_voltage=params.get("battery_rated_voltage"),
                default_load_mode=params.get("default_load_mode"),
                equalize_duration=params.get("equalize_duration"),
                boost_duration=params.get("boost_duration"),
                battery_discharge=params.get("battery_discharge"),
                battery_charge=params.get("battery_charge"),
                charging_mode=params.get("charging_mode")
            )
            return battery_params

        except Exception as e:
            print("Erreur lors de la récupération des paramètres de batterie :", e)

        # Si aucune donnée n'est trouvée ou en cas d'erreur
        return None

# A SUPPRIMER
    # def save_local_data(self, data):
    #     """Sauvegarde les données dans un fichier local."""
    #     if not os.path.exists(Config.LOCAL_STORAGE_PATH):
    #         with open(Config.LOCAL_STORAGE_PATH, 'w') as f:
    #             json.dump([], f)

    #     with open(Config.LOCAL_STORAGE_PATH, 'r+') as f:
    #         local_data = json.load(f)
    #         local_data.append(data)
    #         f.seek(0)
    #         json.dump(local_data, f)

    # def sync_local_data_to_cloud(self):
    #     """Synchronise les données locales avec InfluxDB Cloud."""
    #     if not os.path.exists(Config.LOCAL_STORAGE_PATH):
    #         return

    #     with open(Config.LOCAL_STORAGE_PATH, 'r') as f:
    #         local_data = json.load(f)

    #     for data in local_data:
    #         try:
    #             self.write_api.write(
    #                 bucket=Config.INFLUXDB_BUCKET,
    #                 org=Config.INFLUXDB_ORG,
    #                 record=data
    #             )
    #         except Exception as e:
    #             print(f"Erreur de synchronisation des données vers le cloud : {e}")
    #             return

    #     # Si toutes les données sont synchronisées, on vide le fichier
    #     os.remove(Config.LOCAL_STORAGE_PATH)