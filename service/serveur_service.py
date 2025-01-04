from flask import jsonify
import psutil


class ServeurService:
    def status(self):
        return jsonify({"message": "Kammthaar est en ligne"}), 200
    
    def get_system_info(self):
    # Collecte des données
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        temperatures = psutil.sensors_temperatures()
        # Gestion des températures du CPU
        if 'cpu_thermal' in temperatures:
            temperature = temperatures['cpu_thermal'][0].current  # Utilise la propriété `.current`
        else:
            temperature = 'N/A'  # Valeur par défaut si 'cpu_thermal' n'existe pas

        # Envoi des données sous forme de JSON
        data = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_info.percent,
            'disk_usage': disk_usage.percent,
            'temperature': temperature
        }
        return jsonify(data)