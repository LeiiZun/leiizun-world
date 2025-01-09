import requests

SERVER_URL = "http://127.0.0.1:5000"  # URL du serveur Flask

def send_command(command):
    url = f"{SERVER_URL}/execute_command"
    try:
        response = requests.get(url, params={"command": command})
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Erreur {response.status_code} : {response.text}")
    except Exception as e:
        print(f"Erreur lors de la connexion au serveur : {e}")

# Exemple : Envoie de la commande "capture_camera"
send_command("capture_camera")
