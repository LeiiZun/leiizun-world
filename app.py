from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Route principale pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Route pour capturer des commandes
@app.route("/execute_command", methods=["GET"])
def execute_command():
    command = request.args.get("command")
    if command == "capture_camera":
        print("Commande 'capture_camera' reçue !")
        # Ajoute ici le code pour capturer la caméra
        return jsonify({"status": "success", "message": "Commande capturée avec succès"})
    else:
        return jsonify({"status": "error", "message": "Commande inconnue"})

if __name__ == "__main__":
    app.run(debug=True)
