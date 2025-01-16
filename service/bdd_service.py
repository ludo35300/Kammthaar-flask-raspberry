import logging, influxdb_client, time, requests, json
from datetime import datetime, timezone
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from constantes.authentification import Authentification


class BDDService:
     # Initialisation de la BDD InfluxDB
    def __init__(self):
        try:
            self.client = influxdb_client.InfluxDBClient(url=Authentification.INFLUXDB_URL, token=Authentification.INFLUXDB_TOKEN, org=Authentification.INFLUXDB_ORG)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
            
            logging.basicConfig(level=logging.DEBUG, encoding='utf-8')
        except Exception as e:
            logging.error(f"Erreur de connexion à InfluxDB 2.0': {e}")
            
    def save_data(self, measurement_name, tags, fields, timestamp):
        """
        Fonction générique pour sauvegarder des données dans InfluxDB.
        
        Args:
            measurement_name (str): Nom de la mesure (par exemple, "battery_data").
            tags (dict): Tags pour la mesure (par exemple, {"device": "battery"}).
            fields (dict): Champs à enregistrer dans la mesure.
            timestamp (datetime): Heure à laquelle les données doivent être associées.
        """
        point = Point(measurement_name) \
            .tag("device", tags.get("device", "unknown_device"))  # Utilise un tag générique par défaut
        
        # Ajoute les champs à l'instance du point
        for field_name, field_value in fields.items():
            point = point.field(field_name, field_value)
        
        point = point.time(timestamp)
        result = self.write_api.write(bucket=Authentification.INFLUXDB_BUCKET, org=Authentification.INFLUXDB_ORG, record=point)
        logging.info(f"Données de {measurement_name} sauvegardées avec succès")
        time.sleep(1)
            
    
            
    # Enregistrement du status de la batterie
    def save_battery_status(self, batteryStatus: dict, timestamp):
        fields = {
            "voltage": batteryStatus["voltage"],
            "current": batteryStatus["current"],
            "power": batteryStatus["power"],
            "state_of_charge": batteryStatus["state_of_charge"],
            "temperature": batteryStatus["temperature"],
            "wrong_identifaction_for_rated_voltage": batteryStatus["status"]["wrong_identifaction_for_rated_voltage"],
            "battery_inner_resistence_abnormal": batteryStatus["status"]["battery_inner_resistence_abnormal"],
            "temperature_warning_status": batteryStatus["status"]["temperature_warning_status"],
            "battery_status": batteryStatus["status"]["battery_status"]
        }
        tags = {"device": "batteryStatus"}
        self.save_data("batteryStatus", tags, fields, timestamp)
    
    # Enregistrement du status de charge
    def save_charging_equipment_status(self, chargingEquipmentStatus: dict, timestamp):
        fields = {
            "input_voltage_status": chargingEquipmentStatus["input_voltage_status"],
            "charging_status": chargingEquipmentStatus["charging_status"],
            "running": chargingEquipmentStatus["running"],
            "charging_mosfet_short_circuit": chargingEquipmentStatus["errors"]["charging_mosfet_short_circuit"],
            "charging_or_anti_reverse_mosfet_open_circuit": chargingEquipmentStatus["errors"]["charging_or_anti_reverse_mosfet_open_circuit"],
            "anti_reverse_mosfet_short_circuit": chargingEquipmentStatus["errors"]["anti_reverse_mosfet_short_circuit"],
            "input_over_current": chargingEquipmentStatus["errors"]["input_over_current"],
            "load_over_current": chargingEquipmentStatus["errors"]["load_over_current"],
            "load_short_circuit": chargingEquipmentStatus["errors"]["load_short_circuit"],
            "load_mosfet_short_circuit": chargingEquipmentStatus["errors"]["load_mosfet_short_circuit"],
            "disequilibrium_in_three_circuits": chargingEquipmentStatus["errors"]["disequilibrium_in_three_circuits"],
            "pv_input_short_circuit": chargingEquipmentStatus["errors"]["pv_input_short_circuit"],
            "fault": chargingEquipmentStatus["errors"]["fault"]
        }
        tags = {"device": "chargingEquipmentStatus"}
        self.save_data("chargingEquipmentStatus", tags, fields, timestamp)
    
    # Enregistrement des données du controller MPPT
    def save_controller_data(self, controllerData: dict, timestamp):
        fields = {
            "temperature": controllerData["temperature"],
            "device_over_temperature": controllerData["device_over_temperature"],
            "current_device_time": controllerData["current_device_time"].isoformat(),
        }
        tags = {"device": "controllerData"}
        self.save_data("controllerData", tags, fields, timestamp)
        
    # Enregistrement des données du controller MPPT
    def save_daily_statistics(self, dailyStatistics: dict, timestamp):
        fields = {
            "maximum_battery_voltage_today": dailyStatistics["maximum_battery_voltage_today"],
            "minimum_battery_voltage_today": dailyStatistics["minimum_battery_voltage_today"],
            "day_time": dailyStatistics["day_time"],
            "night_time": dailyStatistics["night_time"],
        }
        tags = {"device": "dailyStatistics"}
        self.save_data("dailyStatistics", tags, fields, timestamp)
        
    # Enregistrement du status de décharge
    def save_discharging_equipment_status(self, dischargingEquipmentStatus: dict, timestamp):
        fields = {
            "input_voltage_status": dischargingEquipmentStatus["input_voltage_status"],
            "output_power_load": dischargingEquipmentStatus["output_power_load"],
            "running": dischargingEquipmentStatus["running"],
            "short_circuit": dischargingEquipmentStatus["errors"]["short_circuit"],
            "unable_to_discharge": dischargingEquipmentStatus["errors"]["unable_to_discharge"],
            "unable_to_stop_discharging": dischargingEquipmentStatus["errors"]["unable_to_stop_discharging"],
            "output_voltage_abnormal": dischargingEquipmentStatus["errors"]["output_voltage_abnormal"],
            "input_over_voltage": dischargingEquipmentStatus["errors"]["input_over_voltage"],
            "short_circuit_high_voltage_side": dischargingEquipmentStatus["errors"]["short_circuit_high_voltage_side"],
            "boost_over_voltage": dischargingEquipmentStatus["errors"]["boost_over_voltage"],
            "output_over_voltage": dischargingEquipmentStatus["errors"]["output_over_voltage"],
            "fault": dischargingEquipmentStatus["errors"]["fault"]
        }
        tags = {"device": "dischargingEquipmentStatus"}
        self.save_data("dischargingEquipmentStatus", tags, fields, timestamp)
        
    # Enregistrement des statistiques énergétiques
    def save_energy_statistics(self, energyStatistics: dict, timestamp):
        fields = {
            "consumed_today": energyStatistics["consumed_today"],
            "consumed_this_month": energyStatistics["consumed_this_month"],
            "consumed_this_year": energyStatistics["consumed_this_year"],
            "total_consumed": energyStatistics["total_consumed"],
            "generated_today": energyStatistics["generated_today"],
            "generated_this_month": energyStatistics["generated_this_month"],
            "generated_this_year": energyStatistics["generated_this_year"],
            "total_generated": energyStatistics["total_generated"],
        }
        tags = {"device": "energyStatistics"}
        self.save_data("energyStatistics", tags, fields, timestamp)
        
    # Enregistrement des données de consommation
    def save_load_data(self, loadData: dict, timestamp):
        fields = {
            "voltage": loadData["voltage"],
            "current": loadData["current"],
            "power": loadData["power"],
        }
        tags = {"device": "loadData"}
        self.save_data("loadData", tags, fields, timestamp)
        
    # Enregistrement des données du panneau solaire
    def save_solar_data(self, solarData: dict, timestamp):
        fields = {
            "voltage": solarData["voltage"],
            "current": solarData["current"],
            "power": solarData["power"],
            "maximum_voltage_today": solarData["maximum_voltage_today"],
            "minimum_voltage_today": solarData["minimum_voltage_today"],
        }
        tags = {"device": "solarData"}
        self.save_data("solarData", tags, fields, timestamp)
       
    # # Récupération des paramètres de la batterie dans la base de données
    # def get_battery_parameters(self):
    #     query = f'''
    #     from(bucket: "{Authentification.INFLUXDB_BUCKET}")
    #     |> range(start: -10d)   // Durée de recherche
    #     |> filter(fn: (r) => r._measurement == "batterie_parametres")
    #     |> last()              // Dernier enregistrement
    #     '''
    #     try:
    #         result = self.query_api.query(org=Authentification.INFLUXDB_ORG, query=query)
    #         # On initialise un dictionnaire pour stocker les valeurs de paramètres
    #         params = {}

    #         # Parcours des enregistrements retournés par InfluxDB
    #         for table in result:
    #             for record in table.records:
    #                 field = record.get_field()
    #                 value = record.get_value()
    #                 if value is not None:  # Ne prendre que les valeurs non nulles
    #                     params[field] = value

    #         # Validation des données récupérées pour éviter les erreurs
    #         def get_param(key, default=None):
    #             return params.get(key, default)

    #         # Construction de l'instance BatteryParametresData avec des valeurs par défaut en cas de données manquantes
    #         battery_params = BatteryParametresData(
    #             rated_charging_current=int(get_param("rated_charging_current", 0)),
    #             rated_load_current=get_param("rated_load_current", 0),
    #             real_rated_voltage=get_param("real_rated_voltage", "0"),
    #             battery_type=get_param("battery_type", "unknown"),
    #             battery_capacity=get_param("battery_capacity", 0),
    #             temp_compensation_coefficient=get_param("temp_compensation_coefficient", 0.0),
    #             over_voltage_disconnect=get_param("over_voltage_disconnect", 0.0),
    #             charging_limit_voltage=get_param("charging_limit_voltage", 0.0),
    #             over_voltage_reconnect=get_param("over_voltage_reconnect", 0.0),
    #             equalize_charging_voltage=get_param("equalize_charging_voltage", 0.0),
    #             boost_charging_voltage=get_param("boost_charging_voltage", 0.0),
    #             float_charging_voltage=get_param("float_charging_voltage", 0.0),
    #             boost_reconnect_voltage=get_param("boost_reconnect_voltage", 0.0),
    #             low_voltage_reconnect=get_param("low_voltage_reconnect", 0.0),
    #             under_voltage_recover=get_param("under_voltage_recover", 0.0),
    #             under_voltage_warning=get_param("under_voltage_warning", 0.0),
    #             low_voltage_disconnect=get_param("low_voltage_disconnect", 0.0),
    #             discharging_limit_voltage=get_param("discharging_limit_voltage", 0.0),
    #             battery_rated_voltage=get_param("battery_rated_voltage", 0.0),
    #             default_load_mode=get_param("default_load_mode", "default"),
    #             equalize_duration=get_param("equalize_duration", 0),
    #             boost_duration=get_param("boost_duration", 0),
    #             battery_discharge=get_param("battery_discharge", 0.0),
    #             battery_charge=get_param("battery_charge", 0.0),
    #             charging_mode=get_param("charging_mode", "unknown")
    #         )
    #         return battery_params

    #     except Exception as e:
    #         print("Erreur lors de la récupération des paramètres de batterie :", e)
    #         # Si aucune donnée n'est trouvée ou en cas d'erreur, retourner None
    #         return None

    # def delete_measurement(self, measurement_name):
    #     """
    #     Supprime un measurement dans InfluxDB v2.x.

    #     Args:
    #     - measurement_name (str): Le nom du measurement à supprimer.
        
    #     Returns:
    #     - Response (str): Message de la réponse de l'API InfluxDB.
    #     """
    #     url = f"{Authentification.INFLUXDB_URL}/api/v2/delete"
    #     start_time = "1970-01-01T00:00:00Z"  # Date de début fixe
    #     stop_time = datetime.now(timezone.utc).isoformat()  # Date actuelle au format RFC3339Nano

    #     # Construire le corps de la requête
    #     body = {
    #         "predicate": f'_measurement="{measurement_name}"',
    #         "start": start_time,
    #         "stop": stop_time,
    #     }
    #     # Ajouter le token d'authentification dans les headers
    #     headers = {
    #         "Authorization": f"Token {Authentification.INFLUXDB_TOKEN}",
    #         "Content-Type": "application/json",
    #     }
    #     # Ajouter les paramètres de l'URL
    #     params = {
    #         "org": Authentification.INFLUXDB_ORG,
    #         "bucket": Authentification.INFLUXDB_BUCKET,
    #     }

    #     response = requests.post(url, headers=headers, params=params, data=json.dumps(body))

    #     # Vérifier la réponse de la requête
    #     if response.status_code == 204:
    #         return f"Measurement '{measurement_name}' supprimé avec succès."
    #     else:
    #         return f"Erreur: {response.status_code} - {response.text}"