import logging, influxdb_client, time, requests, json
from datetime import datetime, timezone
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from constantes.authentification import Authentification
from models.battery_entity import BatteryData
from models.battery_parametres_entity import BatteryParametresData
from models.battery_status_entity import BatteryStatusData
from models.charging_status_entity import ChargingStatusData
from models.discharging_status_entity import DischargerStatusData
from models.ps_entity import PSData
from models.controller_entity import ControllerData
from models.statistiques_entity import StatistiquesData


class BDDService:
     # Initialisation de la BDD InfluxDB
    def __init__(self):
        try:
            self.client = influxdb_client.InfluxDBClient(url=Authentification.INFLUXDB_URL, token=Authentification.INFLUXDB_TOKEN, org=Authentification.INFLUXDB_ORG, timeout=5000)
            logging.basicConfig(level=logging.DEBUG, encoding='utf-8')
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
        except Exception as e:
            print(f"Erreur de connexion à InfluxDB 2.0': {e}")
            
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
        
        self.write_api.write(bucket=Authentification.INFLUXDB_BUCKET, org=Authentification.INFLUXDB_ORG, record=point)
        logging.info(f"Données de {measurement_name} sauvegardées avec succès")
        time.sleep(1)
            
    
            
    # Enregistrement des données de la batterie
    def save_battery_data(self, battery_data: BatteryData, timestamp):
        fields = {
            "battery_voltage": battery_data.battery_voltage,
            "battery_amperage": battery_data.battery_amperage,
            "battery_power": battery_data.battery_power,
            "battery_temp": battery_data.battery_temp,
            "battery_pourcent": battery_data.battery_pourcent
        }
        tags = {"device": "battery"}
        self.save_data("battery_data", tags, fields, timestamp)
        
    # Enregistrement des informations du status de la batterie
    def save_battery_status_data(self, battery_status_data: BatteryStatusData, timestamp):
        fields = {
            "wrong_identifaction_for_rated_voltage": battery_status_data.wrong_identifaction_for_rated_voltage,
            "battery_inner_resistence_abnormal": battery_status_data.battery_inner_resistence_abnormal,
            "temperature_warning_status": battery_status_data.temperature_warning_status,
            "battery_status": battery_status_data.battery_status
        }
        tags = {"device": "battery_status_data"}
        self.save_data("battery_status_data", tags, fields, timestamp)
    
    # Enregistrement des données du panneau solaire
    def save_ps_data(self, ps_data: PSData, timestamp):
        fields = {
            "voltage": ps_data.voltage,
            "amperage": ps_data.amperage,
            "power": ps_data.power
        }
        tags = {"device": "solar_panel"}
        self.save_data("ps_data", tags, fields, timestamp)

    #  Enregistrement des données du controller MPPT
    def save_controller_data(self, controller_data: ControllerData, timestamp):
        fields = {
            "voltage": controller_data.voltage,
            "amperage": controller_data.amperage,
            "power": controller_data.power,
            "temperature": controller_data.temperature,
            "day_time": controller_data.day_time,
            "night_time": controller_data.night_time,
        }
        tags = {"device": "controller_data"}
        self.save_data("controller_data", tags, fields, timestamp)
        

    # Enregistrement des statistiques
    def save_statistiques_data(self, statistiques_data: StatistiquesData, timestamp):
        fields = {
            "max_battery_voltage_today": statistiques_data.max_battery_voltage_today,
            "min_battery_voltage_today": statistiques_data.min_battery_voltage_today,
            "max_ps_voltage_today": statistiques_data.max_ps_voltage_today,
            "min_ps_voltage_today": statistiques_data.min_ps_voltage_today,
            "consumed_energy_today": statistiques_data.consumed_energy_today,
            "consumed_energy_month": statistiques_data.consumed_energy_month,
            "consumed_energy_year": statistiques_data.consumed_energy_year,
            "consumed_energy_total": statistiques_data.consumed_energy_total,
            "generated_energy_today": statistiques_data.generated_energy_today,
            "generated_energy_month": statistiques_data.generated_energy_month,
            "generated_energy_year": statistiques_data.generated_energy_year,
            "generated_energy_total": statistiques_data.generated_energy_total
        }
        tags = {"device": "statistiques_data"}
        self.save_data("statistiques_data", tags, fields, timestamp)
        
    # Enregistrement des données de status de la charge
    def save_charging_status_data(self, charging_status_data: ChargingStatusData, timestamp):
        fields = {
            "input_voltage_status": charging_status_data.input_voltage_status,
            "charging_mosfet_is_short_circuit": charging_status_data.charging_mosfet_is_short_circuit,
            "charging_or_anti_reverse_mosfet_is_open_circuit": charging_status_data.charging_or_anti_reverse_mosfet_is_open_circuit,
            "anti_reverse_mosfet_is_short_circuit": charging_status_data.anti_reverse_mosfet_is_short_circuit,
            "input_over_current": charging_status_data.input_over_current,
            "load_over_current": charging_status_data.load_over_current,
            "load_short_circuit": charging_status_data.load_short_circuit,
            "load_mosfet_short_circuit": charging_status_data.load_mosfet_short_circuit,
            "disequilibrium_in_three_circuits": charging_status_data.disequilibrium_in_three_circuits,
            "pv_input_short_circuit": charging_status_data.pv_input_short_circuit,
            "charging_status": charging_status_data.charging_status,
            "fault": charging_status_data.fault,
            "running": charging_status_data.running
        }
        tags = {"device": "charging_status_data"}
        self.save_data("charging_status_data", tags, fields, timestamp)
        
    # Enregistrement des données de statut de la batterie
    def save_discharging_status_data(self, discharging_status_data: DischargerStatusData, timestamp):
        fields = {
            "input_voltage_status": discharging_status_data.input_voltage_status,
            "output_power_load": discharging_status_data.output_power_load,
            "short_circuit": discharging_status_data.short_circuit,
            "unable_to_discharge": discharging_status_data.unable_to_discharge,
            "unable_to_stop_discharging": discharging_status_data.unable_to_stop_discharging,
            "output_voltage_abnormal": discharging_status_data.output_voltage_abnormal,
            "input_over_voltage": discharging_status_data.input_over_voltage,
            "short_circuit_in_high_voltage_side": discharging_status_data.short_circuit_in_high_voltage_side,
            "boost_over_voltage": discharging_status_data.boost_over_voltage,
            "output_over_voltage": discharging_status_data.output_over_voltage,
            "fault": discharging_status_data.fault,
            "running": discharging_status_data.running
        }
        tags = {"device": "discharging_status_data"}
        self.save_data("discharging_status_data", tags, fields, timestamp)

        
    # Enregistrement des paramètres de la batterie
    def save_battery_parameters(self, battery_parametres: BatteryParametresData, timestamp, isConnected):
        # Préparer les données pour les champs
        fields = {
            "rated_charging_current": battery_parametres.rated_charging_current,
            "rated_load_current": battery_parametres.rated_load_current,
            "real_rated_voltage": battery_parametres.real_rated_voltage.replace("V", "").strip(),
            "battery_type": battery_parametres.battery_type,
            "battery_capacity": battery_parametres.battery_capacity,
            "temp_compensation_coefficient": battery_parametres.temp_compensation_coefficient,
            "over_voltage_disconnect": battery_parametres.over_voltage_disconnect,
            "charging_limit_voltage": battery_parametres.charging_limit_voltage,
            "over_voltage_reconnect": battery_parametres.over_voltage_reconnect,
            "equalize_charging_voltage": battery_parametres.equalize_charging_voltage,
            "boost_charging_voltage": battery_parametres.boost_charging_voltage,
            "float_charging_voltage": battery_parametres.float_charging_voltage,
            "boost_reconnect_voltage": battery_parametres.boost_reconnect_voltage,
            "low_voltage_reconnect": battery_parametres.low_voltage_reconnect,
            "under_voltage_recover": battery_parametres.under_voltage_recover,
            "under_voltage_warning": battery_parametres.under_voltage_warning,
            "low_voltage_disconnect": battery_parametres.low_voltage_disconnect,
            "discharging_limit_voltage": battery_parametres.discharging_limit_voltage,
            "battery_rated_voltage": float(battery_parametres.real_rated_voltage.replace("V", "")),
            "default_load_mode": battery_parametres.default_load_mode,
            "equalize_duration": battery_parametres.equalize_duration,
            "boost_duration": battery_parametres.boost_duration,
            "battery_discharge": battery_parametres.battery_discharge,
            "battery_charge": battery_parametres.battery_charge,
            "charging_mode": battery_parametres.charging_mode
        }

        tags = {"device": "batterie_parametres"}
        self.save_data("batterie_parametres", tags, fields, timestamp)
        
   

    # Récupération des paramètres de la batterie dans la base de données
    def get_battery_parameters(self):
        query = f'''
        from(bucket: "{Authentification.INFLUXDB_BUCKET}")
        |> range(start: -10d)   // Durée de recherche
        |> filter(fn: (r) => r._measurement == "batterie_parametres")
        |> last()              // Dernier enregistrement
        '''
        try:
            result = self.query_api.query(org=Authentification.INFLUXDB_ORG, query=query)
            # On initialise un dictionnaire pour stocker les valeurs de paramètres
            params = {}

            # Parcours des enregistrements retournés par InfluxDB
            for table in result:
                for record in table.records:
                    field = record.get_field()
                    value = record.get_value()
                    if value is not None:  # Ne prendre que les valeurs non nulles
                        params[field] = value

            # Validation des données récupérées pour éviter les erreurs
            def get_param(key, default=None):
                return params.get(key, default)

            # Construction de l'instance BatteryParametresData avec des valeurs par défaut en cas de données manquantes
            battery_params = BatteryParametresData(
                rated_charging_current=int(get_param("rated_charging_current", 0)),
                rated_load_current=get_param("rated_load_current", 0),
                real_rated_voltage=get_param("real_rated_voltage", "0"),
                battery_type=get_param("battery_type", "unknown"),
                battery_capacity=get_param("battery_capacity", 0),
                temp_compensation_coefficient=get_param("temp_compensation_coefficient", 0.0),
                over_voltage_disconnect=get_param("over_voltage_disconnect", 0.0),
                charging_limit_voltage=get_param("charging_limit_voltage", 0.0),
                over_voltage_reconnect=get_param("over_voltage_reconnect", 0.0),
                equalize_charging_voltage=get_param("equalize_charging_voltage", 0.0),
                boost_charging_voltage=get_param("boost_charging_voltage", 0.0),
                float_charging_voltage=get_param("float_charging_voltage", 0.0),
                boost_reconnect_voltage=get_param("boost_reconnect_voltage", 0.0),
                low_voltage_reconnect=get_param("low_voltage_reconnect", 0.0),
                under_voltage_recover=get_param("under_voltage_recover", 0.0),
                under_voltage_warning=get_param("under_voltage_warning", 0.0),
                low_voltage_disconnect=get_param("low_voltage_disconnect", 0.0),
                discharging_limit_voltage=get_param("discharging_limit_voltage", 0.0),
                battery_rated_voltage=get_param("battery_rated_voltage", 0.0),
                default_load_mode=get_param("default_load_mode", "default"),
                equalize_duration=get_param("equalize_duration", 0),
                boost_duration=get_param("boost_duration", 0),
                battery_discharge=get_param("battery_discharge", 0.0),
                battery_charge=get_param("battery_charge", 0.0),
                charging_mode=get_param("charging_mode", "unknown")
            )
            return battery_params

        except Exception as e:
            print("Erreur lors de la récupération des paramètres de batterie :", e)
            # Si aucune donnée n'est trouvée ou en cas d'erreur, retourner None
            return None

    def delete_measurement(self, measurement_name):
        """
        Supprime un measurement dans InfluxDB v2.x.

        Args:
        - measurement_name (str): Le nom du measurement à supprimer.
        
        Returns:
        - Response (str): Message de la réponse de l'API InfluxDB.
        """
        url = f"{Authentification.INFLUXDB_URL}/api/v2/delete"
        start_time = "1970-01-01T00:00:00Z"  # Date de début fixe
        stop_time = datetime.now(timezone.utc).isoformat()  # Date actuelle au format RFC3339Nano

        # Construire le corps de la requête
        body = {
            "predicate": f'_measurement="{measurement_name}"',
            "start": start_time,
            "stop": stop_time,
        }
        # Ajouter le token d'authentification dans les headers
        headers = {
            "Authorization": f"Token {Authentification.INFLUXDB_TOKEN}",
            "Content-Type": "application/json",
        }
        # Ajouter les paramètres de l'URL
        params = {
            "org": Authentification.INFLUXDB_ORG,
            "bucket": Authentification.INFLUXDB_BUCKET,
        }

        response = requests.post(url, headers=headers, params=params, data=json.dumps(body))

        # Vérifier la réponse de la requête
        if response.status_code == 204:
            return f"Measurement '{measurement_name}' supprimé avec succès."
        else:
            return f"Erreur: {response.status_code} - {response.text}"