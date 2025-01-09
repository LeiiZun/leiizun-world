import cv2
import requests

SERVER_URL = "http://127.0.0.1:5000/upload_frame"  # Change l'URL si tu utilises Render

def send_video():
    cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut
    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur lors de la capture vidéo.")
            break

        # Encode l'image en JPEG pour l'envoyer
        _, buffer = cv2.imencode(".jpg", frame)

        try:
            # Envoie l'image au serveur Flask
            response = requests.post(SERVER_URL, files={"frame": buffer.tobytes()})
            if response.status_code != 200:
                print("Erreur lors de l'envoi de l'image :", response.text)
        except requests.exceptions.RequestException as e:
            print("Erreur de connexion au serveur :", e)

    cap.release()

if __name__ == "__main__":
    send_video()
