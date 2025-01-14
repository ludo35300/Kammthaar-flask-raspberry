import logging, influxdb_client, time, requests, json
from datetime import datetime, timezone
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from constantes.authentification import Authentification

from entity.batteryStatus_entity import BatteryStatus


class BDDService:
     # Initialisation de la BDD InfluxDB
    def __init__(self):
        try:
            self.client = influxdb_client.InfluxDBClient(url=Authentification.INFLUXDB_URL, token=Authentification.INFLUXDB_TOKEN, org=Authentification.INFLUXDB_ORG)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
            
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
            
        timestamp_obj = datetime.fromisoformat(timestamp)
        timestamp_ns = int(timestamp_obj.timestamp() * 1e9)
        point = point.time(timestamp_ns)
        result = self.write_api.write(bucket=Authentification.INFLUXDB_BUCKET, org=Authentification.INFLUXDB_ORG, record=point)
        logging.info(f"Données de {measurement_name} sauvegardées avec succès")
        time.sleep(1)