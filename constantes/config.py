class Config:
    
    # Informations de configuration du controlleur MPPT connecté au Raspberry Pi
    MODBUS_PORT = "/dev/ttyXRUSB0"  # Port Modbus de la connexion au RS485
    MODBUS_SLAVE = 1
    
    # Intervalle de 10 minutes pour la synchronisation
    SYNC_INTERVAL = 600
    
    # Fichier ou les enregistrements soit effectués
    LOCAL_STORAGE_PATH = "local_data.json"