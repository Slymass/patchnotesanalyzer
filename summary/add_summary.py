import sys
import os
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment

def add_summary(master_filename):
    """
    Ajoute une feuille 'Résumé' sans tableau Excel.
    - Deux colonnes : 'Catégorie' et 'Nombre'
    - Évite les erreurs de tableaux Excel corrompus
    """

    if not os.path.exists(master_filename):
        print(f"[ERREUR] Le fichier '{master_filename}' n'existe pas.")
        return

    print("\n[INFO] Création d'une feuille 'Résumé' vide sans tableau dans le fichier Master...")

    # Charger le fichier Excel
    wb = load_workbook(master_filename)

    # Suppression propre de la feuille "Résumé" si elle existe déjà
    if "Résumé" in wb.sheetnames:
        del wb["Résumé"]
    ws_summary = wb.create_sheet("Résumé", 0)

    # Définition des en-têtes
    headers = ["Catégorie", "Nombre"]
    ws_summary.append(headers)

    # Appliquer un style aux en-têtes
    for col_num, header in enumerate(headers, start=1):
        col_letter = get_column_letter(col_num)
        ws_summary[f"{col_letter}1"].font = Font(bold=True)
        ws_summary[f"{col_letter}1"].alignment = Alignment(horizontal="center")

    # Ajustement des colonnes
    ws_summary.column_dimensions["A"].width = 25
    ws_summary.column_dimensions["B"].width = 15

    # Sauvegarde propre sans tableau
    wb.save(master_filename)
    print(f"[SUCCÈS] Feuille 'Résumé' ajoutée à '{master_filename}' avec succès, sans tableau.")

if __name__ == "__main__":
    # Vérifier si un fichier Master a été passé en argument
    if len(sys.argv) < 2:
        print("[ERREUR] Aucun fichier Master spécifié.")
        sys.exit(1)

    master_file = sys.argv[1]
    add_summary(master_file)
