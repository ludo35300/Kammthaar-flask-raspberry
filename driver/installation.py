import subprocess
import os

def run_command(command):
    """Exécute une commande système et affiche la sortie"""
    try:
        print(f"Exécution de la commande: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {command}")
        print(e.stderr)

def installation_driver():
    """Effectue toutes les étapes pour recharger le pilote"""
    
    # Vérifie si le pilote est chargé
    run_command("sudo modprobe xr_usb_serial_common")
    
    # Décharge les périphériques USB
    run_command("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind")
    
    # Désactive les pilotes
    run_command("sudo rmmod cdc_acm")
    run_command("sudo rmmod cdc_xr_usb_serial")
    run_command("sudo rmmod xr_serial")
    run_command("sudo rmmod usbserial")
    run_command("sudo rmmod xr_usb_serial_common")
    
    # Dirige vers le dossier du pilote
    driver_dossier = "/xr_usb_serial" 
    os.chdir(driver_dossier)
    
    # Nettoyer, compiler et installer le pilote
    run_command("sudo make clean")
    run_command("sudo make")
    run_command("sudo make install")
    
    # Recharge le pilote xr_usb_serial
    run_command("sudo modprobe xr_usb_serial_common")
    
    # Rattache les périphériques USB
    run_command("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind")

if __name__ == "__main__":
    installation_driver()
