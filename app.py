from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/execute_command', methods=['GET'])
def execute_command():
    command = request.args.get('command')
    
    if command == "capture_camera":
        # Exemple de traitement pour capture_camera
        print("Commande 'capture_camera' reçue !")
        return jsonify({"status": "success", "message": "Commande 'capture_camera' exécutée"})
    else:
        return jsonify({"status": "error", "message": f"Commande inconnue : {command}"})

if __name__ == "__main__":
    app.run(debug=True)
