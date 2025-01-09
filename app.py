from flask import Flask, render_template_string, request, Response
import cv2

app = Flask(__name__)

# Commande pour exécuter les actions sur le client
@app.route('/execute_command', methods=['GET'])
def execute_command():
    command = request.args.get('command')
    if command == "shutdown":
        return "Commande : éteindre le PC exécutée."
    elif command == "capture_camera":
        return "Commande : capture caméra exécutée."
    elif command == "custom_command":
        return "Commande personnalisée exécutée."
    else:
        return "Commande inconnue."

# Route pour le flux vidéo
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Génère les frames du flux vidéo
def gen_frames():
    camera = cv2.VideoCapture(0)  # 0 correspond à la caméra par défaut
    # Définir la résolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not camera.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # Encode la frame en JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                # Retourne la frame encodée
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()

# Page d'accueil avec l'interface utilisateur
@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Leiizun World</title>
        <style>
            body {
                background-color: #222;
                color: #fff;
                text-align: center;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            header {
                background-color: #f57c00;
                padding: 20px;
                margin-bottom: 20px;
            }
            header h1 {
                margin: 0;
                font-size: 36px;
            }
            button {
                background-color: #f57c00;
                border: none;
                color: white;
                padding: 15px 30px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px;
                cursor: pointer;
                border-radius: 5px;
            }
            button:hover {
                background-color: #e64a19;
            }
            #video-container {
                margin-top: 20px;
                display: flex;
                justify-content: center;
            }
            #video-feed {
                border: 2px solid #f57c00;
                border-radius: 10px;
                width: 960px;
                height: 720px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Leiizun World</h1>
        </header>
        <button onclick="triggerAction('shutdown')">Éteindre le PC</button>
        <button onclick="triggerAction('capture_camera')">Capture de la caméra</button>
        <button onclick="triggerAction('custom_command')">Commande personnalisée</button>
        
        <div id="video-container">
            <h2 style="color: #f57c00;">Flux caméra en direct</h2>
            <br>
            <img id="video-feed" src="/video_feed" alt="Flux vidéo">
        </div>

        <script>
            function triggerAction(command) {
                fetch(`/execute_command?command=${command}`)
                    .then(response => response.text())
                    .then(data => alert(data))
                    .catch(error => console.error(error));
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
