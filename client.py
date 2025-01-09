import cv2
import socketio
import base64

# Initialise le client WebSocket
sio = socketio.Client()

# Connecte au serveur
sio.connect('https://leiizun-world.onrender.com')  # Remplace par ton URL Render

def stream_video():
    cap = cv2.VideoCapture(0)  # Utilise la caméra par défaut

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode l'image en JPEG, puis en base64
        _, buffer = cv2.imencode('.jpg', frame)
        frame_encoded = base64.b64encode(buffer).decode('utf-8')

        # Envoie l'image encodée au serveur
        sio.emit('video_stream', {'data': frame_encoded})

    cap.release()

if __name__ == '__main__':
    try:
        stream_video()
    except KeyboardInterrupt:
        print("Streaming arrêté.")
    finally:
        sio.disconnect()
