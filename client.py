import requests

# URL du serveur Flask
SERVER_URL = "http://127.0.0.1:5000/execute_command"

def send_command(command):
    try:
        response = requests.get(SERVER_URL, params={"command": command})
        print("Réponse du serveur :", response.text)
    except Exception as e:
        print(f"Erreur : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    command = "capture_camera"  # Modifie cette commande selon tes besoins
    send_command(command)
