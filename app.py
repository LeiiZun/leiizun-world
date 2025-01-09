from flask import Flask, render_template, Response
import socketio
import base64

app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Stockage temporaire de l'image envoyée par le client
video_frame = None

@app.route('/')
def index():
    """Rendu de la page HTML."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Envoie du flux vidéo aux utilisateurs."""
    def generate():
        global video_frame
        while True:
            if video_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       video_frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@sio.on('video_stream')
def video_stream(data):
    """Réception des images encodées en base64 depuis le client."""
    global video_frame
    video_frame = base64.b64decode(data['data'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
