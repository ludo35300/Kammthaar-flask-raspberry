import threading, time, json, os, traceback, requests

from datetime import datetime
from constantes.config import Config
from models.battery_entity import BatteryData
from models.battery_parametres_entity import BatteryParametresData
from models.battery_status_entity import BatteryStatusData
from models.controller_entity import ControllerData
from models.ps_entity import PSData
from models.statistiques_entity import StatistiquesData
from service.batterie_parametres_service import BatterieParametresService
from service.battery_service import BatterieService
from service.bdd_service import BDDService
from service.mppt_service import MPPTService
from service.ps_service import PSService
from service.statistiques_service import StatistiquesService

class RecordService:
    
    def __init__(self):
        # Initialisation des services
        self.bdd_service = BDDService()
        self.ps_service = PSService()
        self.batterie_service = BatterieService()
        self.statistiques_service = StatistiquesService()
        self.mppt_service = MPPTService()
        # Pour continuer l'enregistrement en cas d'arrêt de l'application
        self.stop_event = threading.Event()
        # Verrouillage du fichier de sauvegarde local pour éviter les conflits 
        self.file_lock = threading.Lock()
       

    def is_connected(self):
        """Vérifie si l'application est connectée à Internet en vérifiant la connexion à la BDD."""
        try:
            requests.get(Config.INFLUXDB_URL, timeout=3)
            return True
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
                # Lecture des données
                ps_data = self.ps_service.read_ps_data()
                battery_data = self.batterie_service.read_battery_data()
                controller_data = self.mppt_service.read_controller_data()
                statistiques_data = self.statistiques_service.read_statistique_data()
                new_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "battery_data": battery_data.to_dict(),
                        "ps_data": ps_data.to_dict(),
                        "controller_data": controller_data.to_dict(),
                        "statistiques_data": statistiques_data.to_dict(),
                    },
                }
                # Sauvegarde locale des données
                self.save_local_data(new_data)

                # Vérification de la connexion à Internet
                if self.is_connected():
                    print("Connexion Internet détectée. Synchronisation des données...")
                    self.sync_local_data_to_cloud()

            except Exception as e:
                print(f"Erreur lors du traitement périodique : {e}")
                traceback.print_exc()

            print(f"Pause de {interval} secondes avant le prochain cycle...")
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
                        print("Fichier JSON vide ou corrompu, initialisation des données.")
                        local_data = []

                    # Ajout des nouvelles données
                    local_data.append(data)

                    # Réécriture des données dans le fichier
                    f.seek(0)
                    json.dump(local_data, f, indent=4)
                    f.truncate()  # Supprime tout contenu résiduel au-delà de la nouvelle écriture

                print("Données sauvegardées localement.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde locale : {e}")
            traceback.print_exc()

            
    def sync_local_data_to_cloud(self):
        """Synchronise les données locales avec InfluxDB et vide le fichier local."""
        try:
            with self.file_lock:
                if not os.path.exists(Config.LOCAL_STORAGE_PATH):
                    print("Aucune donnée locale à synchroniser.")
                    return

                if os.path.getsize(Config.LOCAL_STORAGE_PATH) == 0:  # Vérifie si le fichier est vide
                    print("Fichier local vide, aucune donnée à synchroniser.")
                    return
                
                with open(Config.LOCAL_STORAGE_PATH, "r") as f:
                    
                    local_data = json.load(f)

                for entry in local_data:
                    try:
                        timestamp = entry["timestamp"]
                        self.bdd_service.save_battery_data(BatteryData(**entry["data"]["battery_data"]), timestamp)
                        self.bdd_service.save_ps_data(PSData(**entry["data"]["ps_data"]), timestamp)
                        self.bdd_service.save_controller_data(ControllerData(**entry["data"]["controller_data"]), timestamp)
                        self.bdd_service.save_statistiques_data(StatistiquesData(**entry["data"]["statistiques_data"]), timestamp)
                    except Exception as e:
                        print(f"Erreur lors de la synchronisation d'une entrée : {e}")
                        traceback.print_exc()

                # Vider le fichier après synchronisation
                open(Config.LOCAL_STORAGE_PATH, "w").close()
                print("Données locales synchronisées et fichier local vidé.")
        except Exception as e:
            print(f"Erreur lors de la synchronisation des données locales : {e}")
            traceback.print_exc()