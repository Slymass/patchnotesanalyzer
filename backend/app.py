from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Active CORS pour permettre les requêtes depuis React

UPLOAD_FOLDER = "backend/uploads"
RESULTS_FOLDER = "backend/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"html"}
SYSTEMS = {"Sciforma", "BC"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files or "system" not in request.form: 
        return jsonify({"error": "Fichier HTML et système requis"}), 400
    
    file = request.files["file"]
    system = request.form["system"]
    
    if file.filename == "" or not allowed_file(file.filename) or system not in SYSTEMS:
        return jsonify({"error": "Fichier invalide ou système non reconnu"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    try:
        subprocess.run(["python", "main.py", filepath, system], check=True, text=True, encoding="utf-8")
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Erreur lors du traitement : {e}"}), 500
    
    master_file = filename.rsplit('.', 1)[0] + "_Master.xlsx"
    master_path = os.path.join(RESULTS_FOLDER, master_file)
    if not os.path.exists(master_path):
        return jsonify({"error": "Fichier Master non généré"}), 500
    
    return jsonify({"message": "Traitement réussi", "download_url": f"/download/{master_file}"})

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    path = os.path.join(RESULTS_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "Fichier non trouvé"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
