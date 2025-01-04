class Config:
    
    # Informations de configuration du controlleur MPPT connecté au Raspberry Pi
    MODBUS_PORT = "/dev/ttyXRUSB0"  # Port Modbus de la connexion au RS485
    MODBUS_SLAVE = 1
    
    # Informations de connexion a la basse de données InfluDB 2.0
    INFLUXDB_URL = "http://87.106.191.213:8086"
    INFLUXDB_TOKEN = "jV6SOFGxj66921WQaqF31GAyozmVHnhJbmbTGQ-oHcB5GnzGXbsqDWUUr3IoRVc0TE-GjaMN5UJ8GS6ifnQYFg=="
    INFLUXDB_ORG = "kammthaar"
    INFLUXDB_BUCKET = "solar_data"
    
    # Intervalle de 10 minutes pour la synchronisation
    SYNC_INTERVAL = 600
    
    # Fichier ou les enregistrements soit effectués lorsque le Raspberry Pi n'est pas connecté à Internet 
    # ( et ne peux donc pas enregistrer les information dans la base de données)
    LOCAL_STORAGE_PATH = "local_data.json"