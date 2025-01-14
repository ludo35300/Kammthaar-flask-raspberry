import threading, time, json, os, traceback, requests, logging
from datetime import datetime
from constantes.authentification import Authentification
from constantes.config import Config

from service.bdd_service import BDDService
from service.batteryStatus_service import BatterieStatusService
from service.chargingEquipmentStatus_service import ChargingEquipmentStatusService
from service.controllerData_service import ControllerDataService
from service.dailyStatistics_service import DailyStatisticsService
from service.dischargingEquipmentStatus_service import DischargingEquipmentStatusService
from service.energyStatistics_service import EnergyStatisticsService
from service.loadData_service import LoadDataService
from service.solarData_service import SolarDataService


class RecordService:
    def __init__(self):
        # Initialisation des services
        self.bdd_service = BDDService()
        self.batteryStatus_service = BatterieStatusService()
        self.chargingEquipmentStatus_service = ChargingEquipmentStatusService()
        self.controllerData_service = ControllerDataService()
        self.dailyStatistics_service = DailyStatisticsService()
        self.dischargingEquipmentStatus_service = DischargingEquipmentStatusService()
        self.energyStatistics_service = EnergyStatisticsService()
        self.loadData_service = LoadDataService()
        self.solarData_service = SolarDataService()
        # Pour continuer l'enregistrement en cas d'arrêt de l'application
        self.stop_event = threading.Event()
        # Verrouillage du fichier de sauvegarde local pour éviter les conflits 
        self.file_lock = threading.Lock()
        
        
    def is_connected(self):
        """Vérifie si l'application est connectée à Internet en vérifiant la connexion à la BDD."""
        try:
            response = requests.get(f"{Authentification.INFLUXDB_URL}/health", timeout=3)
            return response.status_code == 200
        except requests.ConnectionError:
            return False
        
    def start_periodic_recording(self, interval=600):
        """Démarre l'enregistrement périodique dans un thread séparé."""
        thread = threading.Thread(target=self.record_data_periodically, args=(interval,))
        thread.daemon = True  # Arrêter le thread avec l'application principale
        thread.start()
        
    def record_data_periodically(self, interval=600):
        while not self.stop_event.is_set():
            try:
                # Récupération des données
                new_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "batteryStatus": self.batteryStatus_service.read_battery_status_data(),
                        "chargingEquipmentStatus": self.chargingEquipmentStatus_service.read_charging_equipment_status_data(),
                        "controllerData": self.controllerData_service.read_controller_data(),
                        "dailyStatistics": self.dailyStatistics_service.read_daily_statistics_data(),
                        "dischargingEquipmentStatus": self.dischargingEquipmentStatus_service.read_discharging_equipment_status_data(),
                        "energyStatistics": self.energyStatistics_service.read_energy_statistics_data(),
                        "loadData": self.loadData_service.read_load_data(),
                        "solarData": self.solarData_service.read_solar_data()
                    },
                }
                # Sauvegarde locale des données
                self.save_local_data(new_data)
                # Vérification de la connexion à Internet
                if self.is_connected():
                    logging.info("Connexion Internet détectée. Synchronisation des données...")
                    self.sync_local_data_to_cloud()
            except Exception as e:
                logging.error(f"Erreur lors du traitement périodique : {e}")
                traceback.print_exc()
            logging.info(f"Pause de {interval} secondes avant le prochain cycle...")
            time.sleep(interval)

    def save_local_data(self, data):
        """Sauvegarde les données localement dans un fichier JSON."""
        try:
            with self.file_lock:
                # Si le fichier n'existe pas, on le crée avec une liste vide
                if not os.path.exists(Config.LOCAL_STORAGE_PATH):
                    with open(Config.LOCAL_STORAGE_PATH, "w") as f:
                        json.dump([], f)
                with open(Config.LOCAL_STORAGE_PATH, "r+") as f:
                    try:
                        # Lecture des données existantes
                        local_data = json.load(f)
                    except json.JSONDecodeError:
                        # Si le fichier est vide ou corrompu, on initialise une liste vide
                        logging.info(f"Fichier JSON vide ou corrompu, initialisation des données.")
                        local_data = []
                    local_data.append(data)
                    # Réécriture des données dans le fichier
                    f.seek(0)
                    json.dump(local_data, f, indent=4)
                    f.truncate()  # Supprime tout contenu résiduel au-delà des nouvelles données
                logging.info(f"Données sauvegardées localement.")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde locale : {e}")
            traceback.print_exc()
            
    def sync_local_data_to_cloud(self):
        """Synchronise les données locales avec InfluxDB et vide le fichier local."""
        try:
            with self.file_lock:
                # Si le fichier n'existe pas ou s'il est vide
                if not os.path.exists(Config.LOCAL_STORAGE_PATH) or os.path.getsize(Config.LOCAL_STORAGE_PATH) == 0:
                    return
                with open(Config.LOCAL_STORAGE_PATH, "r") as f:
                    local_data = json.load(f)
                for entry in local_data:
                    timestamp = entry["timestamp"]
                    categories = entry["data"]
                    for measurement, content in categories.items():
                        # Préparer les tags et les champs
                        tags = {"device": measurement}
                        fields = {}
                        # Parcourir les sous-clés pour structurer les champs et éviter les sous-dictionnaires
                        for key, value in content.items():
                            if isinstance(value, dict):
                                # Si le champ contient des sous-champs (e.g., "status"), on aplatit
                                for sub_key, sub_value in value.items():
                                    field_name = f"{key}_{sub_key}"  # Exemple : "status_battery_status"
                                    fields[field_name] = sub_value
                            else:
                                fields[key] = value
                        # Sauvegarder dans InfluxDB
                        try:
                            self.bdd_service.save_data(
                                measurement_name=measurement,
                                tags=tags,
                                fields=fields,
                                timestamp=timestamp
                            )
                        except Exception as e:
                            logging.error(f"Erreur lors de la sauvegarde de {measurement}: {e}")
                # Vider le fichier après synchronisation
                open(Config.LOCAL_STORAGE_PATH, "w").close()
                logging.info(f"Données locales synchronisées et fichier local vidé.")
        except Exception as e:
            logging.error(f"Erreur lors de la synchronisation des données locales : {e}")
            traceback.print_exc()