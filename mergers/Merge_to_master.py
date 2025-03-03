import sys
import os
import pandas as pd
import subprocess
from openpyxl import load_workbook

def merge_to_master(base_name, correctifs_file, enhancements_file, master_filename):
    """
    Fusionne les fichiers Correctifs et Enhancements en un seul fichier Master.
    - Ajoute une colonne 'Test Status' à chaque feuille.
    - Vérifie que les fichiers existent avant de les inclure.
    """

    print("\n[INFO] Fusion des fichiers en un seul Master...")

    files = {
        "Correctifs": correctifs_file,
        "Enhancements": enhancements_file
    }

    with pd.ExcelWriter(master_filename, engine="openpyxl") as writer:
        for sheet_name, file in files.items():
            if os.path.exists(file):
                df = pd.read_excel(file)
                df["Test Status"] = ""  # Ajout de la colonne Test Status
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"[SUCCÈS] Feuille '{sheet_name}' ajoutée au fichier maître avec colonne 'Test Status'.")
            else:
                print(f"[AVERTISSEMENT] Fichier '{file}' introuvable. Feuille '{sheet_name}' ignorée.")

    print(f"\n[INFO] Fichier Master '{master_filename}' généré avec succès.")

    # Ajouter la feuille Résumé via `add_summary.py`
    print("\n[INFO] Ajout du résumé avec `add_summary.py`...")
    try:
        subprocess.run(["python", "summary/add_summary.py", master_filename], check=True)
        print(f"[SUCCÈS] Résumé ajouté avec succès à '{master_filename}'.")
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Problème lors de l'ajout du résumé : {e}")

if __name__ == "__main__":
    # Vérifie si les arguments nécessaires sont bien passés
    if len(sys.argv) < 4:
        print("[ERREUR] Arguments manquants. Utilisation : python merge_to_master.py base_name correctifs_file enhancements_file master_filename")
        sys.exit(1)

    base_name = sys.argv[1]
    correctifs_file = sys.argv[2]
    enhancements_file = sys.argv[3]
    master_filename = sys.argv[4]

    merge_to_master(base_name, correctifs_file, enhancements_file, master_filename)
